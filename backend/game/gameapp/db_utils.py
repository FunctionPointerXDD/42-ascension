import logging
from gameapp.models import TempMatch, TempMatchRoom, TempMatchRoomUser, TempMatchUser
from django.db.models import Min


logger = logging.getLogger(__name__)


def clear_room(room_name: str):
    logger.info(f"clear_room room_name={room_name}")

    temp_room = TempMatchRoom.objects.get(room_name=room_name)
    room_user = TempMatchRoomUser.objects.filter(temp_match_room_id=temp_room.id)
    room_user.delete()

    temp_match = TempMatch.objects.filter(match_room_id=temp_room.id)
    temp_match_user = TempMatchUser.objects.filter(temp_match__in=temp_match)

    temp_match_user.delete()
    temp_match.delete()

    temp_room.delete()


def get_room_user_or_none(user_id: int):
    try:
        temp_match_room_user = TempMatchRoomUser.objects.get(user_id=user_id)
    except:
        temp_match_room_user = None
    return temp_match_room_user


def get_matchid_user_in(user_id: int) -> int:
    user_min_match = TempMatch.objects.filter(tempmatchuser__user_id=user_id).aggregate(
        round=Min("round")
    )["round"]
    match_user = TempMatchUser.objects.filter(
        user_id=user_id, temp_match__round=user_min_match
    ).get()
    return match_user.temp_match.id


def delete_match(match_id: int) -> None | int:
    matches = TempMatch.objects.filter(id=match_id).all()
    if len(matches) == 0:
        return None

    matchroom_id: int = matches[0].match_room_id  # type: ignore
    matches.delete()
    return matchroom_id


def delete_matchroom(matchroom_id: int):
    TempMatchRoom.objects.filter(id=matchroom_id).delete()
