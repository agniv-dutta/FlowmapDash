EVENT_TYPES = frozenset({"page_view", "click"})

PAGINATION_DEFAULTS = {
    "page": 1,
    "per_page": 20,
}

PAGINATION_MAX_PER_PAGE = 200

SORT_OPTIONS = frozenset({"created_at", "last_activity", "timestamp"})
