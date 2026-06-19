import logging

from flask import Blueprint, request, jsonify

from app.models import EventCreate
from app.services.event_service import EventService

events_bp = Blueprint("events", __name__)
logger = logging.getLogger(__name__)


@events_bp.route("", methods=["POST"])
def record_event():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    try:
        event_data = EventCreate(**data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        result = EventService.record(event_data)
        return jsonify(result), 201
    except Exception:
        logger.exception("Failed to record event")
        return jsonify({"error": "Internal server error"}), 500


@events_bp.route("", methods=["GET"])
def list_events():
    session_id = request.args.get("session_id")
    if not session_id:
        return jsonify({"error": "session_id query parameter is required"}), 400

    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)

    try:
        result = EventService.list_by_session(session_id, offset=offset, limit=limit)
        return jsonify(result), 200
    except Exception:
        logger.exception("Failed to list events")
        return jsonify({"error": "Internal server error"}), 500
