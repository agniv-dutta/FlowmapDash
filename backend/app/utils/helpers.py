from datetime import datetime, timezone


def parse_iso_datetime(value) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise ValueError(f"Cannot parse datetime: {value}")


def serialize_document(doc) -> dict:
    result = {}
    for field_name in doc._fields_ordered:
        value = getattr(doc, field_name, None)
        if isinstance(value, datetime):
            value = value.isoformat()
        result[field_name] = value
    return result
