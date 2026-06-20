import logging
from datetime import datetime, timedelta
from mongoengine import get_connection

from flask import Blueprint, request, jsonify, current_app

from app.services.session_service import SessionService
from app.services.event_service import EventService
from app.exceptions import ValidationError, NotFoundError
from app import log_query_performance

v1_sessions_bp = Blueprint("v1_sessions", __name__)
logger = logging.getLogger(__name__)


@v1_sessions_bp.route("", methods=["GET"])
@log_query_performance
def list_sessions():
    limit = request.args.get("limit", 20, type=int)
    offset = request.args.get("offset", 0, type=int)
    sort_by = request.args.get("sort_by", "recent")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if limit < 1 or limit > 200:
        raise ValidationError("limit must be between 1 and 200")
    if offset < 0:
        raise ValidationError("offset must be non-negative")
    if sort_by not in ("recent", "most_active"):
        raise ValidationError("sort_by must be 'recent' or 'most_active'")

    # Build aggregation pipeline
    pipeline = [
        {
            '$lookup': {
                'from': 'events',
                'localField': 'sessionId',
                'foreignField': 'sessionId',
                'as': 'events'
            }
        },
        {
            '$addFields': {
                'eventCount': {'$size': '$events'},
                'lastActivity': {'$max': '$events.timestamp'}
            }
        }
    ]

    # Add date filtering
    if start_date or end_date:
        match_stage = {}
        if start_date:
            try:
                start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
                match_stage['createdAt'] = {'$gte': start}
            except ValueError:
                raise ValidationError("Invalid start_date format (use ISO 8601)")
        if end_date:
            try:
                end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                if 'createdAt' in match_stage:
                    match_stage['createdAt']['$lte'] = end
                else:
                    match_stage['createdAt'] = {'$lte': end}
            except ValueError:
                raise ValidationError("Invalid end_date format (use ISO 8601)")
        
        if match_stage:
            pipeline.append({'$match': match_stage})

    # Add sorting
    if sort_by == "recent":
        pipeline.append({'$sort': {'createdAt': -1}})
    else:
        pipeline.append({'$sort': {'eventCount': -1}})

    # Add pagination
    pipeline.extend([
        {'$skip': offset},
        {'$limit': limit},
        {'$project': {'events': 0}}  # Don't return all events
    ])

    try:
        conn = get_connection()
        db = conn[current_app.config.get("MONGO_DB_NAME", "flowmapdash")]
        sessions = list(db.sessions.aggregate(pipeline))
        
        # Get total count
        count_pipeline = [
            {
                '$lookup': {
                    'from': 'events',
                    'localField': 'sessionId',
                    'foreignField': 'sessionId',
                    'as': 'events'
                }
            },
            {
                '$addFields': {
                    'eventCount': {'$size': '$events'}
                }
            }
        ]
        
        if start_date or end_date:
            count_pipeline.append({'$match': match_stage})
        
        count_pipeline.append({'$count': 'total'})
        count_result = list(db.sessions.aggregate(count_pipeline))
        total = count_result[0]['total'] if count_result else 0

        return jsonify({
            'data': sessions,
            'total': total,
            'offset': offset,
            'limit': limit
        }), 200
    except Exception:
        logger.exception("Failed to list sessions with aggregation")
        raise


@v1_sessions_bp.route("/<session_id>", methods=["GET"])
@log_query_performance
def get_session_detail(session_id):
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)

    if limit < 1 or limit > 200:
        raise ValidationError("limit must be between 1 and 200")

    try:
        conn = get_connection()
        db = conn[current_app.config.get("MONGO_DB_NAME", "flowmapdash")]
        
        # Get session with aggregation
        pipeline = [
            {'$match': {'sessionId': session_id}},
            {
                '$lookup': {
                    'from': 'events',
                    'localField': 'sessionId',
                    'foreignField': 'sessionId',
                    'as': 'events'
                }
            },
            {
                '$addFields': {
                    'eventCount': {'$size': '$events'}
                }
            }
        ]
        
        session_result = list(db.sessions.aggregate(pipeline))
        if not session_result:
            raise NotFoundError(f"Session '{session_id}' not found")
        
        session = session_result[0]
        
        # Get paginated events
        events_pipeline = [
            {'$match': {'sessionId': session_id}},
            {'$sort': {'timestamp': -1}},
            {'$skip': offset},
            {'$limit': limit}
        ]
        
        events = list(db.events.aggregate(events_pipeline))
        
        # Get total events count
        count_pipeline = [
            {'$match': {'sessionId': session_id}},
            {'$count': 'total'}
        ]
        count_result = list(db.events.aggregate(count_pipeline))
        total_events = count_result[0]['total'] if count_result else 0

        return jsonify({
            "session": session,
            "events": events,
            "total_events": total_events,
            "offset": offset,
            "limit": limit,
        }), 200
    except Exception:
        logger.exception("Failed to fetch session detail with aggregation")
        raise


@v1_sessions_bp.route("/seed", methods=["POST"])
def seed_sessions():
    """Create sample data for testing"""
    try:
        conn = get_connection()
        db = conn[current_app.config.get("MONGO_DB_NAME", "flowmapdash")]
        
        # Clear existing data (dev only)
        db.sessions.delete_many({})
        db.events.delete_many({})
        
        # Create 5 sample sessions
        sessions = []
        for i in range(1, 6):
            session_id = f'sess_demo_{str(i).zfill(3)}'
            sessions.append({
                'session_id': session_id,
                'created_at': datetime.now() - timedelta(hours=i),
                'last_activity': datetime.now() - timedelta(hours=i-1),
                'metadata': {'status': 'active' if i <= 2 else 'inactive'},
                'event_count': 0
            })
        
        db.sessions.insert_many(sessions)
        
        # Create sample events for each session
        events = []
        for session in sessions:
            for j in range(5, 15):
                events.append({
                    'event_id': f'evt_{session["session_id"]}_{j}',
                    'session_id': session['session_id'],
                    'event_type': 'page_view' if j % 2 == 0 else 'click',
                    'page_url': f'https://example.com/page/{j}',
                    'timestamp': datetime.now() - timedelta(minutes=j),
                    'coordinates': {'x': 100 + j*10, 'y': 200 + j*5} if j % 2 else None,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'metadata': {}
                })
        
        db.events.insert_many(events)
        
        # Update session event counts
        for session in sessions:
            event_count = db.events.count_documents({'session_id': session['session_id']})
            db.sessions.update_one(
                {'session_id': session['session_id']},
                {'$set': {'event_count': event_count}}
            )
        
        return jsonify({
            'message': 'Sample data created',
            'sessions': len(sessions),
            'events': len(events)
        }), 201
    except Exception as e:
        logger.exception("Failed to seed sample data")
        return jsonify({'error': str(e)}), 500
