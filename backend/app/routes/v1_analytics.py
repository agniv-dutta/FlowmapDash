import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify

from app.models import Session, Event
from app.services.event_service import EventService

v1_analytics_bp = Blueprint("v1_analytics", __name__)
logger = logging.getLogger(__name__)


@v1_analytics_bp.route("/summary", methods=["GET"])
def summary():
    try:
        total_sessions = Session.objects.count()
        total_events = Event.objects.count()
        avg_events = round(total_events / total_sessions, 2) if total_sessions else 0.0

        most_visited = EventService.get_most_visited_pages(limit=10)
        peak_hours = EventService.get_peak_activity_hours()

        return jsonify({
            "total_sessions": total_sessions,
            "total_events": total_events,
            "avg_events_per_session": avg_events,
            "most_visited_pages": most_visited,
            "peak_activity_hours": peak_hours,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }), 200
    except Exception:
        logger.exception("Failed to generate analytics summary")
        raise
