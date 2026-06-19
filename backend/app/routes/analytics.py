import logging
from datetime import datetime, timezone

from flask import Blueprint, request, jsonify

from app.services.event_service import EventService

analytics_bp = Blueprint("analytics", __name__)
logger = logging.getLogger(__name__)


@analytics_bp.route("/event-counts", methods=["GET"])
def event_counts():
    event_type = request.args.get("event_type")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    granularity = request.args.get("granularity", "hour")

    start = None
    if start_date:
        try:
            start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        except ValueError:
            return jsonify({"error": "Invalid start_date format"}), 400

    end = None
    if end_date:
        try:
            end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        except ValueError:
            return jsonify({"error": "Invalid end_date format"}), 400

    try:
        total = EventService.get_event_counts(
            event_type=event_type,
            start=start,
            end=end,
        )
        return jsonify({
            "event_type": event_type or "all",
            "total": total,
            "start_date": start.isoformat() if start else None,
            "end_date": end.isoformat() if end else None,
            "granularity": granularity,
        }), 200
    except Exception as e:
        logger.exception("Failed to compute event counts")
        return jsonify({"error": "Internal server error"}), 500


@analytics_bp.route("/summary", methods=["GET"])
def summary():
    try:
        from app.models import Session, Event
        total_sessions = Session.objects.count()
        total_events = Event.objects.count()
        page_views = Event.objects(event_type="page_view").count()
        clicks = Event.objects(event_type="click").count()

        return jsonify({
            "total_sessions": total_sessions,
            "total_events": total_events,
            "page_views": page_views,
            "clicks": clicks,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }), 200
    except Exception as e:
        logger.exception("Failed to generate summary")
        return jsonify({"error": "Internal server error"}), 500
