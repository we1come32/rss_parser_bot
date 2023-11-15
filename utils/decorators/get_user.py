from typing import Optional

from aiogram.types import Message
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from cachetools.func import ttl_cache

from models import User, engine


@ttl_cache(ttl=5)
def get_user(user_id: int) -> User:
    with Session(engine) as ss:
        if not ss.execute(select(User).where(User.id == user_id)).fetchall():
            ss.execute(insert(User).values([(user_id, False)]))
            ss.commit()
    return ss.execute(select(User).where(User.id == user_id)).fetchone()[0]


def get_user_from_message(msg: Message) -> Optional[User]:
    if msg:
        if msg.from_user:
            return get_user(user_id=msg.from_user.id)
