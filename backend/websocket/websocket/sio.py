import json
import logging
import socketio
from typing import Any

from websocket.envs import FRONTEND_URL

sio = socketio.Server(
    cors_allowed_origins=["https://localhost", f"https://{FRONTEND_URL}"]
)

logger = logging.getLogger(__name__)

ROOM_LISTENERS = "room_listeners"
ROOM_LIST_EVENT = "room_list"
ROOM_CHANGED_EVENT = "room_changed"
START_GAME_EVENT = "start_game"

ROOM_LIMIT_VALID_VALUES = [2, 4, 8, 16]


def sio_emit(event: str, data: dict[str, Any], to: str):
    logger.info(f"emit event={event}, data={json.dumps(data)}, to={to}")
    return sio.emit(event, data=data, to=to)


def _sio_enter_room(sid: str, room: str):
    logger.info(f"sid={sid} enters room={room}")
    sio.enter_room(sid, room)


def _sio_leave_room(sid: str, room: str):
    logger.info(f"sid={sid} leaves room={room}")
    sio.leave_room(sid, room)


def sio_enter_room_by_id(sid: str, room: str):
    _sio_leave_room(sid, ROOM_LISTENERS)
    _sio_enter_room(sid, room)


def sio_leave_room_by_room(sid: str, room: str):
    _sio_leave_room(sid, room)
    _sio_enter_room(sid, ROOM_LISTENERS)


def sio_enter_room_by_init(sid: str):
    _sio_enter_room(sid, ROOM_LISTENERS)
