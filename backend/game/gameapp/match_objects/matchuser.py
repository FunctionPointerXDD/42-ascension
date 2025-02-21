import logging
from typing import TypedDict

from exceptions.CustomException import InternalException

AI_ID = -1
AI_NAME = "AI"

logger = logging.getLogger(__name__)


class MatchUser(TypedDict):
    is_ai: bool
    sid: str
    id: int
    name: str


class RealUser(MatchUser):
    pass


class AiUser(MatchUser):
    pass


def get_aidto(sid: str):
    return AiUser(is_ai=True, sid=sid, id=AI_ID, name=AI_NAME)


def get_realdto(sid: str, user_id: int, user_name: str):
    return RealUser(is_ai=False, sid=sid, id=user_id, name=user_name)


def get_dto(is_ai: bool, sid: str, user_id: int, user_name: str | None):
    if is_ai:
        return get_aidto(sid)
    else:
        if user_name is None:
            logger.error(
                "When `is_ai` is False, expected `user_name` not to be None, but got None!"
            )
            raise InternalException()
        return get_realdto(sid, user_id, user_name)
