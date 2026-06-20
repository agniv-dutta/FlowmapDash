import logging
from flask_socketio import SocketIO, emit, join_room, leave_room

logger = logging.getLogger(__name__)

# Initialize SocketIO with CORS support
socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')
    emit('connection_response', {'data': 'Connected to FlowmapDash'})


@socketio.on('subscribe_session')
def handle_subscribe(data):
    """Handle session subscription for real-time updates"""
    session_id = data.get('sessionId')
    if session_id:
        join_room(session_id)
        logger.info(f'Client subscribed to session: {session_id}')
        emit('subscribed', {'sessionId': session_id})


@socketio.on('unsubscribe_session')
def handle_unsubscribe(data):
    """Handle session unsubscription"""
    session_id = data.get('sessionId')
    if session_id:
        leave_room(session_id)
        logger.info(f'Client unsubscribed from session: {session_id}')
        emit('unsubscribed', {'sessionId': session_id})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')


def emit_new_event(session_id: str, event_data: dict):
    """Emit new event to subscribers of a specific session"""
    try:
        socketio.emit('new_event', event_data, room=session_id)
        logger.debug(f'Emitted new event for session {session_id}')
    except Exception as e:
        logger.error(f'Failed to emit event: {e}')


def emit_session_update(session_id: str, session_data: dict):
    """Emit session update to subscribers"""
    try:
        socketio.emit('session_update', session_data, room=session_id)
        logger.debug(f'Emitted session update for session {session_id}')
    except Exception as e:
        logger.error(f'Failed to emit session update: {e}')


def emit_analytics_update(analytics_data: dict):
    """Emit analytics update to all connected clients"""
    try:
        socketio.emit('analytics_update', analytics_data)
        logger.debug('Emitted analytics update to all clients')
    except Exception as e:
        logger.error(f'Failed to emit analytics update: {e}')
