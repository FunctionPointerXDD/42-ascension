"""
WSGI config for websocket project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import json
import logging
import os
import socketio
from django.core.wsgi import get_wsgi_application
from socketio.exceptions import ConnectionRefusedError
from typing import Any, List, TypedDict

from exceptions.CustomException import (
    CustomException,
    BadRequestFieldException,
    InternalException,
    UnauthenticatedException,
    WebSocketAlreadyRoomJoinedException,
    WebSocketRoomNotAdminException,
    WebSocketRoomNotFullException,
    WebSocketRoomNotJoinedException,
)
from websocket.decorators import event_on
from websocket.envs import JWT_URL, GAME_URL
from websocket.requests import post
from websocket.room.room import Room
from websocket.room.roomuser import RoomUser, RoomUserJson
from websocket.room.room_manager import ROOM_MANAGER
from websocket.sio import (
    ROOM_LIMIT_VALID_VALUES,
    START_GAME_EVENT,
    sio,
    sio_emit,
    sio_enter_room_by_id,
    sio_enter_room_by_init,
    sio_leave_room_by_room,
)
from websocket.userdict import UserDict
from websocket.utils import (
    fetch_username,
    get_int,
    get_joined_room,
    get_str,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websocket.settings")

application = get_wsgi_application()
application = socketio.WSGIApp(sio, application)

logger = logging.getLogger(__name__)

sid_list = []


class TokenDto(TypedDict):
    access_token: str
    refresh_token: str


class PeopleListJson(TypedDict):
    people: List[RoomUserJson]


user_dict = UserDict()


def get_session_info(sid: str) -> int:
    with sio.session(sid) as sess:
        user_id: int | None = sess["user_id"]

    if user_id is None:
        raise UnauthenticatedException()

    return user_id


def _get_user_id_from_jwt(jwt: str) -> int:
    res = post(f"{JWT_URL}/jwt/check", json={"jwt": jwt, "skip_2fa": False})
    if not res.ok:
        logger.error(f"post failed, content={res.text}")
        raise ConnectionRefusedError(res.text)

    json = res.json()
    return json["user_id"]


def _connect(sid: str, environ, auth: dict[str, Any]):
    logger.info(f"auth={json.dumps(auth)}")

    jwt = get_str(auth, "jwt")
    user_id = _get_user_id_from_jwt(jwt)
    user_name = fetch_username(user_id)
    logger.info(f"from _get_user_id_from_Jwt: user_id={user_id}, user_name={user_name}")

    with sio.session(sid) as sess:
        sess["user_id"] = user_id
        sess["user_name"] = user_name

    user_add_ret = user_dict.add(user_id, RoomUser(sid, user_id, user_name))
    if not user_add_ret:
        logger.info(f"userid={user_id} is in dict -> user.found")
        raise ConnectionRefusedError("user.found")

    sio_enter_room_by_init(sid)
    ROOM_MANAGER.emit_to_listeners(to=sid)


@event_on("connect")
def connect(sid: str, environ, auth: dict[str, Any]):
    try:
        return _connect(sid, environ, auth)
    except CustomException as e:
        raise ConnectionRefusedError(e.msg)
    except ConnectionRefusedError as e:
        raise e
    except Exception as e:
        logger.error(f"While connecting, type = {type(e)}")
        logger.exception(e)
        raise ConnectionRefusedError("internal_error")


@event_on("disconnect")
def disconnect(sid: str, reason):
    user_id = get_session_info(sid)
    logger.info(f"sid={sid}, user_id={user_id} Disconnecting")

    joined_room = get_joined_room(sid)
    try:
        if joined_room is not None:
            ROOM_MANAGER.remove_user(joined_room, user_id)
    except Exception as e:
        logger.error("While disconnecting, error")
        logger.exception(e)

    user_dict.remove(user_id)

    if joined_room is not None:
        ROOM_MANAGER.emit_room_changed(joined_room, user_dict)


@event_on("name")
def sio_name(sid: str, data: dict[str, Any] | None = None):
    with sio.session(sid) as sess:
        user_name = sess["user_name"]

    return {"name": user_name}


@event_on("make_room")
def sio_make_room(sid: str, data: dict[str, Any]):
    user_id = get_session_info(sid)

    room_name = get_str(data, "room_name", blank=False)
    room_limit = get_int(data, "room_limit")
    if room_limit not in ROOM_LIMIT_VALID_VALUES:
        raise BadRequestFieldException("room_limit")

    joined_room_id = get_joined_room(sid)
    if joined_room_id is not None:
        raise WebSocketAlreadyRoomJoinedException()

    logger.info(
        f"Server got make_room! title={room_name}, room_limit={room_limit}, user_id={user_id}"
    )
    room = Room(room_name=room_name, room_limit=room_limit, admin=user_id)
    ROOM_MANAGER.add_room(room)
    sio_enter_room_by_id(sid, room.room_id)

    ROOM_MANAGER.emit_room_changed(room.room_id, user_dict)


@event_on("enter_room")
def on_enter_room(sid: str, data: dict[str, Any]):
    user_id = get_session_info(sid)

    room_id = get_str(data, "room_id")
    joined_room_id = get_joined_room(sid)
    if joined_room_id is not None:
        raise WebSocketAlreadyRoomJoinedException()

    ROOM_MANAGER.add_user(room_id, user_id)

    sio_enter_room_by_id(sid, room_id)
    ROOM_MANAGER.emit_room_changed(room_id, user_dict)


@event_on("leave_room")
def sio_leave_room(sid: str, data: dict[str, Any]):
    user_id = get_session_info(sid)

    room_id = get_joined_room(sid)
    if room_id is None:
        logger.info("joined_room len = 0, user is not joined in any room")
        raise WebSocketRoomNotJoinedException()

    ROOM_MANAGER.remove_user(room_id, user_id)

    sio_leave_room_by_room(sid, room_id)
    ROOM_MANAGER.emit_room_changed(room_id, user_dict)


@event_on("start_game")
def sio_start_game(sid: str, data: dict[str, Any]):
    user_id = get_session_info(sid)

    room_id = get_joined_room(sid)
    if room_id is None:
        logger.info("joined_room len = 0, user is not joined in any room")
        raise WebSocketRoomNotJoinedException()

    room = ROOM_MANAGER._get_room(room_id)
    if room is None:
        raise InternalException()
    elif not room.is_full():
        raise WebSocketRoomNotFullException()
    elif not room.is_admin(user_id):
        raise WebSocketRoomNotAdminException()

    resp = post(
        f"{GAME_URL}/_internal/game",
        json={
            "room_name": room.room_name,
            "users": room.people_list_to_json(user_dict),
        },
    )
    if not resp.ok:
        logger.error(f"resp error! {resp.text}")
        raise InternalException()

    user_emit_datas: list[tuple[str, TokenDto]] = []

    for user_id in room.user_list:
        resp = post(f"{JWT_URL}/jwt/token", {"user_id": user_id, "twofa_delete": False})
        if not resp.ok:
            raise CustomException(resp.text, resp.status_code)
        resp_json = resp.json()
        user_emit_datas.append(
            (
                user_dict.get(user_id).sid,
                TokenDto(
                    access_token=resp_json["access_token"],
                    refresh_token=resp_json["refresh_token"],
                ),
            )
        )

    for sid, token_dto in user_emit_datas:
        sio_emit(
            START_GAME_EVENT,
            {
                "accessToken": token_dto["access_token"],
                "refreshToken": token_dto["refresh_token"],
            },
            to=sid,
        )
