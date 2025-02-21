import threading
import copy
from typing import List, TypedDict, TYPE_CHECKING

from exceptions.CustomException import (
    InternalException,
    WebSocketRoomNotFoundException,
)
from websocket.room.room import Room
from websocket.room.roomuser import RoomUserJson
from websocket.sio import sio_emit, ROOM_LISTENERS, ROOM_LIST_EVENT, ROOM_CHANGED_EVENT

if TYPE_CHECKING:
    from websocket.userdict import UserDict


class PeopleListJson(TypedDict):
    people: List[RoomUserJson]


class RoomManager:
    room_dict: dict[str, Room]

    def __init__(self) -> None:
        self.room_dict = {}
        self.lock = threading.Lock()

    def room_list_to_json(self):
        """
        Aquire lock
        """
        with self.lock:
            room_json_list = [room.to_json() for room in self.room_dict.values()]
            return {"room": room_json_list}

    def add_room(self, room: Room):
        """
        Aquire lock
        """
        with self.lock:
            if room.room_id in self.room_dict:
                raise InternalException()
            self.room_dict[room.room_id] = room

    def remove_room(self, room: Room):
        """
        Aquire lock
        """
        with self.lock:
            del self.room_dict[room.room_id]

    def _get_room(self, room_id: str) -> Room | None:
        """
        Aquire lock
        """
        with self.lock:
            if room_id in self.room_dict:
                return self.room_dict[room_id]
            return None

    def add_user(self, room_id: str, user_id: int):
        room = self._get_room(room_id)
        if room is None:
            raise WebSocketRoomNotFoundException()
        if not room.is_valid():
            self.remove_room(room)
            raise WebSocketRoomNotFoundException()
        room.add_user(user_id)

    def remove_user(self, room_id: str, user_id: int):
        room = self._get_room(room_id)
        if room is None:
            raise WebSocketRoomNotFoundException()
        if not room.is_valid():
            self.remove_room(room)
            raise WebSocketRoomNotFoundException()

        room.remove_user(user_id)
        if not room.is_valid():
            self.remove_room(room)

    def people_list_to_json(
        self, room_id: str, user_dict: "UserDict"
    ) -> PeopleListJson:
        room = self._get_room(room_id)
        if room is None:
            return {"people": []}
        return {"people": room.people_list_to_json(user_dict)}

    def emit_to_listeners(self, to: str | None = None):
        if to is None:
            to = ROOM_LISTENERS

        sio_emit(ROOM_LIST_EVENT, self.room_list_to_json(), to=to)

    def emit_room_changed(self, room_id: str, user_dict: "UserDict"):
        sio_emit(
            ROOM_CHANGED_EVENT,
            self.people_list_to_json(room_id, user_dict),  # type: ignore
            to=room_id,
        )
        self.emit_to_listeners()


ROOM_MANAGER = RoomManager()
