import logging
from datetime import datetime

from flask import Blueprint, request, jsonify

from app.services.session_service import SessionService
from app.services.event_service import EventService
from app.exceptions import ValidationError, NotFoundError

v1_sessions_bp = Blueprint("v1_sessions", __name__)
logger = logging.getLogger(__name__)


@v1_sessions_bp.route("", methods=["GET"])
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

    start = None
    if start_date:
        try:
            start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        except ValueError:
            raise ValidationError("Invalid start_date format (use ISO 8601)")

    end = None
    if end_date:
        try:
            end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        except ValueError:
            raise ValidationError("Invalid end_date format (use ISO 8601)")

    try:
        result = SessionService.list(
            offset=offset,
            limit=limit,
            start_date=start,
            end_date=end,
            sort_by=sort_by,
        )
        return jsonify(result), 200
    except Exception:
        logger.exception("Failed to list sessions")
        raise


@v1_sessions_bp.route("/<session_id>", methods=["GET"])
def get_session_detail(session_id):
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)

    if limit < 1 or limit > 200:
        raise ValidationError("limit must be between 1 and 200")

    session_resp = SessionService.get(session_id)
    if session_resp is None:
        raise NotFoundError(f"Session '{session_id}' not found")

    try:
        events_result = EventService.list_by_session(
            session_id, offset=offset, limit=limit
        )
    except Exception:
        logger.exception("Failed to fetch session events")
        raise

    return jsonify({
        "session": session_resp.model_dump(),
        "events": events_result["events"],
        "total_events": events_result["total"],
        "offset": events_result["offset"],
        "limit": events_result["limit"],
    }), 200
