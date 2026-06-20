import uuid
from datetime import datetime, timezone

from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    DictField,
    IntField,
)
from pydantic import BaseModel, Field, field_validator
from typing import Optional


# ─── Pydantic Schemas ──────────────────────────────────────────────────────

class Coordinate(BaseModel):
    x: float
    y: float


class EventCreate(BaseModel):
    session_id: str
    event_type: str
    page_url: str
    timestamp: Optional[datetime] = None
    coordinates: Optional[Coordinate] = None
    user_agent: Optional[str] = None
    metadata: Optional[dict] = None

    @field_validator("event_type")
    @classmethod
    def validate_event_type(cls, v):
        allowed = {"page_view", "click"}
        if v.lower() not in allowed:
            raise ValueError(f"event_type must be one of {allowed}")
        return v.lower()


class BatchEventCreate(BaseModel):
    events: list[EventCreate]


class EventResponse(BaseModel):
    event_id: str
    session_id: str
    event_type: str
    timestamp: datetime
    page_url: str
    coordinates: Optional[dict] = None
    user_agent: Optional[str] = None


class SessionCreate(BaseModel):
    session_id: Optional[str] = None
    metadata: Optional[dict] = None


class SessionResponse(BaseModel):
    session_id: str
    created_at: datetime
    last_activity: datetime
    duration_seconds: float = 0.0
    metadata: Optional[dict] = None
    event_count: int = 0


class SessionListQuery(BaseModel):
    limit: int = Field(default=20, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sort_by: str = Field(default="recent", pattern="^(recent|most_active)$")


class HeatmapQuery(BaseModel):
    page_url: str
    grid_size: Optional[int] = Field(default=None, ge=10, le=500)


class HeatmapPoint(BaseModel):
    x: float
    y: float
    timestamp: datetime
    session_id: str


class HeatmapBin(BaseModel):
    bin_x: int
    bin_y: int
    x_center: float
    y_center: float
    count: int


class HeatmapResponse(BaseModel):
    page_url: str
    points: Optional[list[HeatmapPoint]] = None
    bins: Optional[list[HeatmapBin]] = None
    total_clicks: int


class AnalyticsSummary(BaseModel):
    total_sessions: int
    total_events: int
    avg_events_per_session: float
    most_visited_pages: list[dict]
    peak_activity_hours: list[dict]


# ─── MongoEngine Documents ─────────────────────────────────────────────────
#
# Indexing Strategy — trade-offs documented per index:
#
# Session collection (~1000 concurrent sessions → manageable size)
# ─────────────────────────────────────────────────────────────
# 1. session_id (unique)
#    Purpose: Fast lookup by session key (primary access pattern).
#    Trade-off: Unique constraint adds write overhead; mandatory for
#    correctness since session_id is the logical PK.
#
# 2. last_activity (background)
#    Purpose: Sort sessions by recency on the sessions list endpoint.
#    Trade-off: Updated on every event → high write rate on this index.
#    Background build avoids blocking reads during creation.
#
# 3. created_at (background)
#    Purpose: Filter sessions by creation date range.
#    Trade-off: Rarely queried alone; useful for date-range filtering.
#    Low cardinality but sufficient for range scans.
#
# 4. event_count (background)
#    Purpose: Sort by "most_active" (desc event_count).
#    Trade-off: Updated atomically (inc) on each event. Write amplification
#    is minimal since the value is small. Supports the top-K pattern well.
#
# Event collection (high-write, high-read — primary workload)
# ────────────────────────────────────────────────────────────
# 1. event_id (unique)
#    Purpose: Guarantees idempotent inserts; used for dedup.
#    Trade-off: O(1) lookup but adds write cost on every insert.
#    UUIDv4 distribution avoids hot spotting on the B-tree.
#
# 2. session_id (background)
#    Purpose: Finds all events for a given session (session detail page).
#    Trade-off: Single-field index covers the session detail query.
#    Selective (few events per session on average) → efficient.
#
# 3. session_id + timestamp (compound, background)
#    Purpose: Ordered event listing per session without in-memory sort.
#    Trade-off: Larger index than single-field session_id. Covers both
#    filter (session_id equality) and sort (timestamp desc). Eliminates
#    the need for a separate sort stage in the query plan.
#
# 4. event_type (background)
#    Purpose: Filter events by type (page_view vs click).
#    Trade-off: Low cardinality (2 values) → issues with query plans
#    (MongoDB may prefer a different index). Used mainly in combination
#    with other filters or for count queries.
#
# 5. timestamp (descending, background)
#    Purpose: Global time-range queries, peak-activity aggregation.
#    Trade-off: Descending order matches the most common sort direction.
#    Large index as timestamp grows monotonically; consider TTL
#    archiving for very large collections (>50M docs).
#
# 6. event_type + timestamp (compound, background)
#    Purpose: Count events of a type within a time range without
#    scanning all docs. Covers the analytics/event-counts endpoint.
#    Trade-off: Larger than single-field event_type. Avoids in-memory
#    sort stage for filtered time-range queries.
#
# 7. page_url + event_type (compound, background)
#    Purpose: Heatmap queries — find all click events for a page.
#    Trade-off: Selective for unique pages (good); for popular pages
#    the index still filters to clicks only, reducing scanned docs.
#    Adding timestamp as a suffix would make it a covering index for
#    the heatmap query but increases index size.
#
# General principles:
# - All non-unique indexes built in background to avoid blocking writes
# - WiredTiger storage compresses index data ~50% on disk
# - For Atlas M10+ clusters, index builds happen on secondaries first
# - Monitor Index Usage in Atlas Performance Advisor for unused indexes
# ─────────────────────────────────────────────────────────────


class Session(Document):
    session_id = StringField(required=True, unique=True, default=lambda: str(uuid.uuid4()))
    created_at = DateTimeField(required=True, default=lambda: datetime.now(timezone.utc))
    last_activity = DateTimeField(required=True, default=lambda: datetime.now(timezone.utc))
    metadata = DictField(default=dict)
    event_count = IntField(default=0)

    meta = {
        "collection": "sessions",
        "indexes": [
            "session_id",
            "last_activity",
            "created_at",
            "event_count",
        ],
        "ordering": ["-last_activity"],
    }

    @property
    def duration_seconds(self) -> float:
        return (self.last_activity - self.created_at).total_seconds()

    def to_response(self) -> SessionResponse:
        return SessionResponse(
            session_id=self.session_id,
            created_at=self.created_at,
            last_activity=self.last_activity,
            duration_seconds=self.duration_seconds,
            metadata=self.metadata,
            event_count=self.event_count,
        )


class Event(Document):
    event_id = StringField(required=True, unique=True, default=lambda: str(uuid.uuid4()))
    session_id = StringField(required=True)
    event_type = StringField(required=True, choices=("page_view", "click"))
    timestamp = DateTimeField(required=True, default=lambda: datetime.now(timezone.utc))
    page_url = StringField(required=True)
    coordinates = DictField(default=None)
    user_agent = StringField(default=None)
    metadata = DictField(default=None)

    meta = {
        "collection": "events",
        "indexes": [
            "event_id",
            "session_id",
            [("session_id", 1), ("timestamp", -1)],
            "event_type",
            [("timestamp", -1)],
            [("event_type", 1), ("timestamp", -1)],
            [("page_url", 1), ("event_type", 1)],
        ],
        "ordering": ["-timestamp"],
    }

    def to_response(self) -> EventResponse:
        return EventResponse(
            event_id=self.event_id,
            session_id=self.session_id,
            event_type=self.event_type,
            timestamp=self.timestamp,
            page_url=self.page_url,
            coordinates=self.coordinates,
            user_agent=self.user_agent,
        )
