import logging
from datetime import datetime
from mongoengine import get_connection

from flask import Blueprint, request, jsonify, current_app

from app.models import EventCreate, BatchEventCreate
from app.services.event_service import EventService
from app.utils.rate_limiter import rate_limit
from app.exceptions import ValidationError
from app import log_query_performance

v1_events_bp = Blueprint("v1_events", __name__)
logger = logging.getLogger(__name__)


@v1_events_bp.route("", methods=["GET"])
@log_query_performance
def list_events():
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    session_id = request.args.get("session_id")
    event_type = request.args.get("event_type")
    page_url = request.args.get("page_url")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if limit < 1 or limit > 200:
        raise ValidationError("limit must be between 1 and 200")
    if offset < 0:
        raise ValidationError("offset must be non-negative")

    # Build match stage for filtering
    match_stage = {}
    
    if session_id:
        match_stage['sessionId'] = session_id
    
    if event_type:
        match_stage['eventType'] = event_type
    
    if page_url:
        match_stage['pageUrl'] = page_url
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            match_stage['timestamp'] = {'$gte': start}
        except ValueError:
            raise ValidationError("Invalid start_date format (use ISO 8601)")
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            if 'timestamp' in match_stage:
                match_stage['timestamp']['$lte'] = end
            else:
                match_stage['timestamp'] = {'$lte': end}
        except ValueError:
            raise ValidationError("Invalid end_date format (use ISO 8601)")

    try:
        conn = get_connection()
        db = conn[current_app.config.get("MONGO_DB_NAME", "flowmapdash")]
        
        # Build aggregation pipeline
        pipeline = []
        
        if match_stage:
            pipeline.append({'$match': match_stage})
        
        pipeline.extend([
            {'$sort': {'timestamp': -1}},
            {'$skip': offset},
            {'$limit': limit}
        ])
        
        events = list(db.events.aggregate(pipeline))
        
        # Get total count
        count_pipeline = []
        if match_stage:
            count_pipeline.append({'$match': match_stage})
        count_pipeline.append({'$count': 'total'})
        
        count_result = list(db.events.aggregate(count_pipeline))
        total = count_result[0]['total'] if count_result else 0

        return jsonify({
            'data': events,
            'total': total,
            'offset': offset,
            'limit': limit
        }), 200
    except Exception:
        logger.exception("Failed to list events with aggregation")
        raise


@v1_events_bp.route("", methods=["POST"])
@rate_limit(capacity=200, refill_rate=20.0)
def ingest_events():
    data = request.get_json(silent=True)
    if not data:
        raise ValidationError("Request body must be JSON")

    if "events" in data:
        return _ingest_batch(data)
    return _ingest_single(data)


def _ingest_single(data: dict):
    try:
        event_data = EventCreate(**data)
    except ValueError as e:
        raise ValidationError(str(e))

    try:
        result = EventService.record(event_data)
        return jsonify(result), 201
    except Exception:
        logger.exception("Failed to record event")
        raise


def _ingest_batch(data: dict):
    try:
        batch = BatchEventCreate(**data)
    except ValueError as e:
        raise ValidationError(str(e))

    if len(batch.events) > 1000:
        raise ValidationError("Batch size cannot exceed 1000 events")

    try:
        results = EventService.record_batch(batch.events)
        succeeded = sum(1 for r in results if "error" not in r)
        return jsonify({
            "ingested": succeeded,
            "failed": len(results) - succeeded,
            "events": results,
        }), 201
    except Exception:
        logger.exception("Failed to process batch events")
        raise
