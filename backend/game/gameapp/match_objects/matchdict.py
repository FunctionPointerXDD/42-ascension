from typing import TYPE_CHECKING
import threading
import logging


if TYPE_CHECKING:
    from .match import Match
    from gameapp.match_objects.matchuser import MatchUser, RealUser


class MatchDict:
    logger = logging.getLogger(__name__)

    match_dict_2: dict[int, "Match"]

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.match_dict_2 = {}

    def __get_match(self, match_id: int) -> "Match":
        with self.lock:
            if match_id not in self.match_dict_2:
                raise KeyError()
            return self.match_dict_2[match_id]

    def delete_match_id(self, match_id: int):
        # self.logger.info("delete match id, get lock")
        with self.lock:
            del self.match_dict_2[match_id]
        # self.logger.info("delete_match_id, get lock finished")

    def clear(self):
        # self.logger.info("clear, get lock")
        with self.lock:
            self.match_dict_2 = {}
        # self.logger.info("clear, get lock finished")

    def user_decided(self, match_id: int, user: "RealUser"):
        mat = self.__get_match(match_id)
        mat.user_decided(user)

    def set_if_not_exists(self, match_id: int, value: "Match"):
        with self.lock:
            if match_id not in self.match_dict_2:
                self.match_dict_2[match_id] = value

    def add_listener(self, match_id1: int, match_id2: int):
        mat1 = self.__get_match(match_id1)
        mat2 = self.__get_match(match_id2)
        mat1.add_listener(mat2)
        mat2.add_listener(mat1)

    def ai_connected(self, match_id: int, sid: str):
        mat = self.__get_match(match_id)
        mat.ai_connected(sid)

    def user_connected(self, match_id, user: "RealUser"):
        mat = self.__get_match(match_id)
        mat.user_connected(user)

    def user_disconnected(self, match_id: int, dto: "RealUser"):
        mat = self.__get_match(match_id)
        mat.user_disconnected(dto)

    # def get(self, match_id: int) -> "Match | None":
    #     self.logger.info("get, get lock")
    #     with self.lock:
    #         if match_id in self.match_dict_2:
    #             ret = self.match_dict_2[match_id]
    #         else:
    #             ret = None
    #     self.logger.info("get, get lock finished")
    #     return ret

    def get_room_by_user_dto(self, user_dto: "MatchUser"):
        # self.logger.info("get_room_by_user_dto, get lock")

        with self.lock:
            ret = None
            for match in self.match_dict_2.values():
                if match.is_user_dto_connected(user_dto):
                    ret = match
                    break
        # self.logger.info("get_room_by_user_dto, get lock finished")
        return ret

    # def __getitem__(self, match_id: int) -> "Match":
    #     self.logger.info("MatchDict GetItem")
    #     ret = self.get(match_id)
    #     if ret is None:
    #         raise KeyError()
    #     return ret

    # def get_dict(self) -> "dict[int, Match]":
    #     self.logger.info("MatchDict GetDict")
    #     return self.match_dict_2


match_dict = MatchDict()
