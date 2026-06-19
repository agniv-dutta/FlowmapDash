import logging
from datetime import datetime, timezone

from mongoengine import DoesNotExist, OperationError, Q

from app.models import Session, SessionResponse

logger = logging.getLogger(__name__)


class SessionService:

    @staticmethod
    def get_or_create(session_id: str = None, metadata: dict = None) -> SessionResponse:
        if session_id:
            try:
                session = Session.objects.get(session_id=session_id)
                session.last_activity = datetime.now(timezone.utc)
                session.save()
                return session.to_response()
            except DoesNotExist:
                pass

        session = Session(
            session_id=session_id,
            metadata=metadata or {},
        ).save()
        logger.info("Created new session: %s", session.session_id)
        return session.to_response()

    @staticmethod
    def get(session_id: str) -> SessionResponse:
        try:
            session = Session.objects.get(session_id=session_id)
            return session.to_response()
        except DoesNotExist:
            logger.warning("Session not found: %s", session_id)
            return None

    @staticmethod
    def list(
        offset: int = 0,
        limit: int = 20,
        start_date: datetime = None,
        end_date: datetime = None,
        sort_by: str = "recent",
    ) -> dict:
        try:
            filters = Q()
            if start_date:
                filters &= Q(created_at__gte=start_date)
            if end_date:
                filters &= Q(created_at__lte=end_date)

            if filters:
                base_qs = Session.objects(filters)
            else:
                base_qs = Session.objects

            total = base_qs.count()

            if sort_by == "most_active":
                order_field = "-event_count"
            else:
                order_field = "-last_activity"

            sessions = (
                base_qs.order_by(order_field)
                .only("session_id", "created_at", "last_activity", "metadata", "event_count")
                .skip(offset)
                .limit(limit)
            )

            return {
                "sessions": [s.to_response().model_dump() for s in sessions],
                "total": total,
                "offset": offset,
                "limit": limit,
            }
        except OperationError as e:
            logger.error("Error listing sessions: %s", e)
            raise

    @staticmethod
    def update_activity(session_id: str):
        try:
            Session.objects(session_id=session_id).update_one(
                set__last_activity=datetime.now(timezone.utc),
                inc__event_count=1,
            )
        except OperationError as e:
            logger.error("Error updating session activity: %s", e)
