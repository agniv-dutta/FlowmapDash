import logging

from flask import Blueprint, request, jsonify

from app.services.event_service import EventService
from app.exceptions import ValidationError

v1_heatmap_bp = Blueprint("v1_heatmap", __name__)
logger = logging.getLogger(__name__)


@v1_heatmap_bp.route("", methods=["GET"])
def get_heatmap():
    page_url = request.args.get("page_url")
    if not page_url:
        raise ValidationError("page_url query parameter is required")

    grid_size = request.args.get("grid_size", type=int)

    if grid_size is not None and (grid_size < 10 or grid_size > 500):
        raise ValidationError("grid_size must be between 10 and 500")

    try:
        result = EventService.get_coordinates_by_page(page_url, grid_size=grid_size)
        return jsonify(result), 200
    except Exception:
        logger.exception("Failed to fetch heatmap data")
        raise
