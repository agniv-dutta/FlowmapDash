import logging
from datetime import datetime, timezone
from collections import Counter

from mongoengine import OperationError

from app.models import Event, EventCreate

logger = logging.getLogger(__name__)


class EventService:

    @staticmethod
    def record(event_data: EventCreate) -> dict:
        try:
            ts = event_data.timestamp or datetime.now(timezone.utc)
            coords = (
                {"x": event_data.coordinates.x, "y": event_data.coordinates.y}
                if event_data.coordinates
                else None
            )
            event = Event(
                session_id=event_data.session_id,
                event_type=event_data.event_type,
                page_url=event_data.page_url,
                timestamp=ts,
                coordinates=coords,
                user_agent=event_data.user_agent,
                metadata=event_data.metadata,
            ).save()

            from app.services.session_service import SessionService

            SessionService.update_activity(event_data.session_id)

            logger.info(
                "Recorded event %s (%s) for session %s",
                event.event_id,
                event.event_type,
                event.session_id,
            )
            return event.to_response().model_dump()
        except OperationError as e:
            logger.error("Error recording event: %s", e)
            raise

    @staticmethod
    def record_batch(events_data: list[EventCreate]) -> list[dict]:
        results = []
        for event_data in events_data:
            try:
                result = EventService.record(event_data)
                results.append(result)
            except Exception as e:
                logger.error("Failed to record event in batch: %s", e)
                results.append(
                    {
                        "error": str(e),
                        "session_id": event_data.session_id,
                        "event_type": event_data.event_type,
                    }
                )
        return results

    @staticmethod
    def list_by_session(
        session_id: str, offset: int = 0, limit: int = 50
    ) -> dict:
        try:
            total = Event.objects(session_id=session_id).count()
            events = (
                Event.objects(session_id=session_id)
                .only(
                    "event_id",
                    "session_id",
                    "event_type",
                    "timestamp",
                    "page_url",
                    "coordinates",
                    "user_agent",
                )
                .order_by("timestamp")
                .skip(offset)
                .limit(limit)
            )
            return {
                "events": [e.to_response().model_dump() for e in events],
                "total": total,
                "offset": offset,
                "limit": limit,
            }
        except OperationError as e:
            logger.error("Error listing events: %s", e)
            raise

    @staticmethod
    def get_event_counts(
        event_type: str = None,
        start: datetime = None,
        end: datetime = None,
    ) -> int:
        try:
            query = {}
            if event_type:
                query["event_type"] = event_type
            if start or end:
                ts_filter = {}
                if start:
                    ts_filter["$gte"] = start
                if end:
                    ts_filter["$lte"] = end
                query["timestamp"] = ts_filter
            return Event.objects(**query).count()
        except OperationError as e:
            logger.error("Error counting events: %s", e)
            raise

    @staticmethod
    def get_coordinates_by_page(page_url: str, grid_size: int = None) -> dict:
        try:
            events = (
                Event.objects(page_url=page_url, event_type="click")
                .only("coordinates", "timestamp", "session_id")
                .order_by("timestamp")
            )

            points = [
                {
                    "x": e.coordinates.get("x", 0) if e.coordinates else 0,
                    "y": e.coordinates.get("y", 0) if e.coordinates else 0,
                    "timestamp": e.timestamp.isoformat(),
                    "session_id": e.session_id,
                }
                for e in events
                if e.coordinates
            ]

            total_clicks = len(points)

            if grid_size and points:
                bins = {}
                for p in points:
                    bx = int(p["x"] // grid_size)
                    by = int(p["y"] // grid_size)
                    key = (bx, by)
                    if key not in bins:
                        bins[key] = {
                            "bin_x": bx,
                            "bin_y": by,
                            "x_center": (bx + 0.5) * grid_size,
                            "y_center": (by + 0.5) * grid_size,
                            "count": 0,
                        }
                    bins[key]["count"] += 1

                return {
                    "page_url": page_url,
                    "bins": sorted(
                        bins.values(), key=lambda b: b["count"], reverse=True
                    ),
                    "total_clicks": total_clicks,
                }

            return {
                "page_url": page_url,
                "points": points,
                "total_clicks": total_clicks,
            }
        except OperationError as e:
            logger.error("Error fetching heatmap data: %s", e)
            raise

    @staticmethod
    def get_most_visited_pages(limit: int = 10) -> list[dict]:
        try:
            pipeline = [
                {"$group": {"_id": "$page_url", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": limit},
                {"$project": {"page_url": "$_id", "count": 1, "_id": 0}},
            ]
            return list(Event.objects.aggregate(pipeline))
        except OperationError as e:
            logger.error("Error getting most visited pages: %s", e)
            raise

    @staticmethod
    def get_peak_activity_hours() -> list[dict]:
        try:
            pipeline = [
                {"$group": {"_id": {"$hour": "$timestamp"}, "count": {"$sum": 1}}},
                {"$sort": {"_id": 1}},
                {"$project": {"hour": "$_id", "count": 1, "_id": 0}},
            ]
            return list(Event.objects.aggregate(pipeline))
        except OperationError as e:
            logger.error("Error getting peak activity hours: %s", e)
            raise
