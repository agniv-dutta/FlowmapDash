import logging

from flask import Blueprint, request, jsonify

from app.models import SessionCreate
from app.services.session_service import SessionService
from app.services.event_service import EventService

sessions_bp = Blueprint("sessions", __name__)
logger = logging.getLogger(__name__)


@sessions_bp.route("", methods=["POST"])
def create_session():
    data = request.get_json(silent=True) or {}
    try:
        session_data = SessionCreate(**data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    try:
        result = SessionService.get_or_create(
            session_id=session_data.session_id,
            metadata=session_data.metadata,
        )
        return jsonify(result.model_dump()), 201
    except Exception:
        logger.exception("Failed to create session")
        return jsonify({"error": "Internal server error"}), 500


@sessions_bp.route("/<session_id>", methods=["GET"])
def get_session(session_id):
    try:
        result = SessionService.get(session_id)
        if result is None:
            return jsonify({"error": "Session not found"}), 404
        return jsonify(result.model_dump()), 200
    except Exception:
        logger.exception("Failed to get session")
        return jsonify({"error": "Internal server error"}), 500


@sessions_bp.route("", methods=["GET"])
def list_sessions():
    limit = request.args.get("limit", 20, type=int)
    offset = request.args.get("offset", 0, type=int)
    sort_by = request.args.get("sort_by", "recent")

    if sort_by not in ("recent", "most_active"):
        sort_by = "recent"

    try:
        result = SessionService.list(
            offset=offset,
            limit=limit,
            sort_by=sort_by,
        )
        return jsonify(result), 200
    except Exception:
        logger.exception("Failed to list sessions")
        return jsonify({"error": "Internal server error"}), 500
