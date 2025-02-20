from typing import TYPE_CHECKING
import threading
import logging


if TYPE_CHECKING:
    from .match import Match
    from gameapp.match_objects.matchuser import MatchUser


class MatchDict:
    logger = logging.getLogger(__name__)
    match_dict_2: dict[int, "Match"]

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.match_dict_2 = {}

    def delete_match_id(self, match_id: int):
        self.logger.info("delete match id, trying to get lock")
        with self.lock:
            del self.match_dict_2[match_id]

    def clear(self):
        self.logger.info("clear, trying to get lock")
        with self.lock:
            self.match_dict_2 = {}

    def get(self, match_id: int) -> "Match | None":
        self.logger.info("get, trying to get lock")
        with self.lock:
            if match_id in self.match_dict_2:
                return self.match_dict_2[match_id]
            return None

    def get_room_by_user_dto(self, user_dto: "MatchUser"):
        with self.lock:
            for match in self.match_dict_2.values():
                if match.is_user_dto_connected(user_dto):
                    return match
            return None

    def get_room_by_userid(self, user_id: int) -> "Match | None":
        with self.lock:
            for match in self.match_dict_2.values():
                if match.is_user_connected(user_id):
                    return match
            return None

    def __getitem__(self, match_id: int) -> "Match":
        self.logger.info("MatchDict GetItem")
        ret = self.get(match_id)
        if ret is None:
            raise KeyError()
        return ret

    def get_dict(self) -> "dict[int, Match]":
        self.logger.info("MatchDict GetDict")
        return self.match_dict_2


match_dict = MatchDict()
