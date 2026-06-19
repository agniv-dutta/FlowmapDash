import logging

from flask import Blueprint, request, jsonify

from app.models import EventCreate, BatchEventCreate
from app.services.event_service import EventService
from app.utils.rate_limiter import rate_limit
from app.exceptions import ValidationError

v1_events_bp = Blueprint("v1_events", __name__)
logger = logging.getLogger(__name__)


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
