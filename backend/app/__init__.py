import os
import logging
import time
from datetime import datetime, timezone
from functools import wraps
import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from mongoengine import connect, disconnect, get_connection
from redis import Redis

from config import Config
from app.utils.logging import setup_logging
from app.utils.middleware import register_middleware
from app.exceptions import register_error_handlers
from app.websocket import socketio

# Initialize Redis client
redis_client = None

# Initialize Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)


def cached(key_prefix, ttl=300):
    """Decorator for caching API responses in Redis"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            global redis_client
            if not redis_client:
                return f(*args, **kwargs)
            
            cache_key = f"{key_prefix}:{request.url}"
            try:
                cached_result = redis_client.get(cache_key)
                if cached_result:
                    return json.loads(cached_result), 200
            except Exception as e:
                logging.warning(f"Cache get failed: {e}")
            
            result = f(*args, **kwargs)
            if isinstance(result, tuple):
                response_data = result[0]
                status_code = result[1]
            else:
                response_data = result
                status_code = 200
            
            try:
                redis_client.setex(cache_key, ttl, json.dumps(response_data))
            except Exception as e:
                logging.warning(f"Cache set failed: {e}")
            
            return result
        return decorated_function
    return decorator


def log_query_performance(func):
    """Decorator for monitoring query performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        
        if duration > 1:  # Log slow queries > 1 second
            logging.warning(f"Slow query {func.__name__}: {duration:.2f}s")
        
        return result
    return wrapper


def create_indexes():
    """Create MongoDB indexes for optimal query performance"""
    try:
        conn = get_connection()
        db = conn[conn.get_database().name]
        
        # Sessions collection indexes
        db.sessions.create_index([('sessionId', 1)], unique=True, sparse=True)
        db.sessions.create_index([('createdAt', -1)])
        db.sessions.create_index([('userId', 1)])
        
        # Events collection indexes
        db.events.create_index([('sessionId', 1), ('timestamp', 1)])
        db.events.create_index([('pageUrl', 1)])
        db.events.create_index([('eventType', 1)])
        db.events.create_index([('timestamp', 1)])
        db.events.create_index([('coordinates.x', '2d')])  # Geospatial for heatmap
        
        logging.info("MongoDB indexes created successfully")
    except Exception as e:
        logging.warning(f"Failed to create indexes: {e}")


def create_app(config_class=Config):
    global redis_client, limiter
    app = Flask(__name__)
    app.config.from_object(config_class)

    setup_logging(app.config.get("LOG_LEVEL", "INFO"))
    app.logger.info("Initializing FlowmapDash backend")

    CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))
    
    # Enable response compression
    Compress(app)

    # Initialize Redis
    redis_url = app.config.get("REDIS_URL")
    if redis_url:
        try:
            redis_client = Redis.from_url(redis_url)
            app.logger.info("Connected to Redis")
        except Exception as e:
            app.logger.warning(f"Failed to connect to Redis: {e}")
            redis_client = None

    # Initialize Flask-Limiter with Redis storage
    if redis_client:
        limiter = Limiter(
            key_func=get_remote_address,
            storage_uri=redis_url,
            default_limits=["100 per minute"]
        )
    else:
        limiter = Limiter(
            key_func=get_remote_address,
            default_limits=["100 per minute"]
        )
    limiter.init_app(app)

    _init_db(app)
    create_indexes()  # Create MongoDB indexes
    register_error_handlers(app)
    register_middleware(app)
    
    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins=app.config.get("CORS_ORIGINS", "*"))

    # Register error handlers for rate limiting and other errors
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({'error': 'Rate limit exceeded'}), 429

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': str(error)}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # Add caching headers to responses
    @app.after_request
    def add_caching(response):
        response.cache_control.max_age = 300  # 5 minute cache
        response.cache_control.public = True
        return response

    from app.routes.v1_events import v1_events_bp
    from app.routes.v1_sessions import v1_sessions_bp
    from app.routes.v1_heatmap import v1_heatmap_bp
    from app.routes.v1_analytics import v1_analytics_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(v1_events_bp, url_prefix="/api/v1/events")
    app.register_blueprint(v1_sessions_bp, url_prefix="/api/v1/sessions")
    app.register_blueprint(v1_heatmap_bp, url_prefix="/api/v1/heatmap")
    app.register_blueprint(v1_analytics_bp, url_prefix="/api/v1/analytics")
    app.register_blueprint(auth_bp)

    # ── health / readiness ──────────────────────────────────────────────

    @app.route("/health")
    @app.route("/api/health")
    def health():
        db_ok = False
        try:
            from mongoengine import get_connection
            conn = get_connection()
            db_ok = conn.admin.command("ping")["ok"] == 1.0
        except Exception:
            pass

        return jsonify({
            "status": "healthy" if db_ok else "degraded",
            "database": "connected" if db_ok else "disconnected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": app.config.get("VERSION", "1.0.0"),
        }), 200 if db_ok else 503

    return app


def _init_db(app):
    mongo_uri = app.config.get("MONGO_URI")
    if not mongo_uri:
        app.logger.warning("MONGO_URI not set, skipping DB connection")
        return

    db_name = app.config.get("MONGO_DB_NAME", "flowmapdash")

    try:
        disconnect(alias="default")
        connect(
            db=db_name,
            host=mongo_uri,
            alias="default",
            connect=False,
            maxpoolsize=app.config.get("MONGO_POOL_SIZE", 50),
            minpoolsize=10,
            serverSelectionTimeoutMS=10000,
            socketTimeoutMS=30000,
            connectTimeoutMS=10000,
            retryWrites=True,
            w="majority",
        )
        app.logger.info(
            "Connected to MongoDB: %s (pool: %s-%s)",
            db_name,
            10,
            app.config.get("MONGO_POOL_SIZE", 50),
        )
    except Exception as e:
        app.logger.error("Failed to connect to MongoDB: %s", e)
