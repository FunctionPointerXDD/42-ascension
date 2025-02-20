from typing import TYPE_CHECKING
import threading
import logging

from .matchuser import get_aidto, MatchUser, RealUser


if TYPE_CHECKING:
    from .match import Match


class MatchDict:
    logger = logging.getLogger(__name__)

    match_dict_2: "dict[int, Match]"

    user_to_connected_matchid: "dict[str, int]"

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.match_dict_2 = {}

        self.lock_user = threading.Lock()
        self.user_to_connected_matchid = {}

    def __get_connected_matchid(self, sid: str) -> int | None:
        with self.lock_user:
            ret = None
            if sid in self.user_to_connected_matchid:
                ret = self.user_to_connected_matchid[sid]
        return ret

    def __set_connected_matchid(self, sid: str, match_id: int):
        with self.lock_user:
            self.user_to_connected_matchid[sid] = match_id

    def __del_connected_matchid(self, sid: str):
        with self.lock_user:
            if sid in self.user_to_connected_matchid:
                del self.user_to_connected_matchid[sid]

    def __get_match(self, match_id: int) -> "Match":
        with self.lock:
            if match_id not in self.match_dict_2:
                raise KeyError()
            return self.match_dict_2[match_id]

    def delete_match_id(self, match_id: int):
        self.logger.info(f"delete match id, id={match_id}")
        # self.logger.info("delete match id, get lock")
        with self.lock:
            if match_id in self.match_dict_2:
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
        self.__set_connected_matchid(sid, match_id)
        mat.ai_connected(sid)

    def user_connected(self, match_id: int, user: "RealUser"):
        mat = self.__get_match(match_id)
        self.__set_connected_matchid(user["sid"], match_id)
        mat.user_connected(user)

    def user_disconnected(self, match_id: int, dto: "RealUser"):
        mat = self.__get_match(match_id)
        self.__del_connected_matchid(dto["sid"])
        mat.user_disconnected(dto)

    def current_status(self):
        ret = ""
        with self.lock:
            for k, v in self.match_dict_2.items():
                ret += f"[{k} users={v.users}/is_with_ai={v.is_with_ai}/disconnected={v.disconnected}/opponent={v.opponent}] "

        return ret

    def get_room_by_user_dto(self, user_dto: "MatchUser") -> "Match | None":
        # self.logger.info("get_room_by_user_dto, get lock")

        connected_matchid = self.__get_connected_matchid(user_dto["sid"])
        if connected_matchid is None:
            return None

        return self.__get_match(connected_matchid)


match_dict = MatchDict()
