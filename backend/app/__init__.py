import os
import logging
from datetime import datetime, timezone

from flask import Flask, jsonify
from flask_cors import CORS
from mongoengine import connect, disconnect

from config import Config
from app.utils.logging import setup_logging
from app.utils.middleware import register_middleware
from app.exceptions import register_error_handlers


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    setup_logging(app.config.get("LOG_LEVEL", "INFO"))
    app.logger.info("Initializing FlowmapDash backend")

    CORS(app, origins=app.config.get("CORS_ORIGINS", "*"))

    _init_db(app)
    register_error_handlers(app)
    register_middleware(app)

    from app.routes.v1_events import v1_events_bp
    from app.routes.v1_sessions import v1_sessions_bp
    from app.routes.v1_heatmap import v1_heatmap_bp
    from app.routes.v1_analytics import v1_analytics_bp

    app.register_blueprint(v1_events_bp, url_prefix="/api/v1/events")
    app.register_blueprint(v1_sessions_bp, url_prefix="/api/v1/sessions")
    app.register_blueprint(v1_heatmap_bp, url_prefix="/api/v1/heatmap")
    app.register_blueprint(v1_analytics_bp, url_prefix="/api/v1/analytics")

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
            serverSelectionTimeoutMS=10000,
            socketTimeoutMS=30000,
            connectTimeoutMS=10000,
            retryWrites=True,
            w="majority",
        )
        app.logger.info(
            "Connected to MongoDB: %s (pool: %s)",
            db_name,
            app.config.get("MONGO_POOL_SIZE"),
        )
    except Exception as e:
        app.logger.error("Failed to connect to MongoDB: %s", e)
