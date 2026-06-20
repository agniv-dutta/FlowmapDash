import logging
from bson import ObjectId
from datetime import datetime

from flask import Blueprint, jsonify

v1_notifications_bp = Blueprint("v1_notifications", __name__)
logger = logging.getLogger(__name__)


@v1_notifications_bp.route("", methods=["GET"])
def get_notifications():
    """Get user notifications"""
    return jsonify({
        'notifications': [
            # In production, would fetch from database
        ]
    }), 200
