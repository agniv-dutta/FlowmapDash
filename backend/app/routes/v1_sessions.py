import logging
from datetime import datetime
from mongoengine import get_connection

from flask import Blueprint, request, jsonify

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
        db = conn[conn.get_database().name]
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
        db = conn[conn.get_database().name]
        
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
