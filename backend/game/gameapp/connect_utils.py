import logging
from typing import TYPE_CHECKING

from exceptions.CustomException import InternalException
from gameapp.db_utils import clear_room
from gameapp.envs import GAMEAI_URL
from gameapp.sio import sio_disconnect
from gameapp.match_objects import Match, match_dict
from gameapp.requests import post
from gameapp.utils import get_match_user_or_none

from gameapp.match_objects.matchuser import RealUser

if TYPE_CHECKING:
    from gameapp.models import TempMatchUser


logger = logging.getLogger(__name__)


def join_match(sid: str, match_user: "TempMatchUser", username: str):
    room_id = match_user.temp_match.id
    is_with_ai = match_user.temp_match.is_with_ai

    user = RealUser(is_ai=False, id=match_user.user.id, name=username, sid=sid)
    match_dict.user_connected(room_id, user)

    if is_with_ai:
        resp = post(f"{GAMEAI_URL}/ai/", json={"match_id": room_id})
        if not resp.ok:
            logger.error(f"POST failed, resp content={resp.text}")
            raise InternalException()
        logger.info(f"request to ai has returned! OK={resp.ok}")


def connect_users(users: "list[RealUser]"):
    logger.info(f"connect_users={users}")

    for u in users:
        match_user = get_match_user_or_none(u["id"])
        if match_user is None:
            raise InternalException()
        elif len(match_user) > 1:
            logger.info(f"len(match_user) = {len(match_user)}")
            raise InternalException()
        join_match(u["sid"], match_user[0], u["name"])


def disconnect_users(room_name: str, users: "list[RealUser]"):
    logger.info(f"disconnect users={users}")

    for u in users:
        try:
            if u["sid"] != "":
                sio_disconnect(u["sid"])
        except Exception as e:
            logger.exception(e)
            logger.error("Skipping this error")

    clear_room(room_name)
