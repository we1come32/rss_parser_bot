from typing import Optional

from aiogram.types import Message
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from models import User, engine


def get_user(msg: Message) -> Optional[User]:
    if msg.from_user:
        with Session(engine) as ss:
            if not ss.execute(select(User).where(User.id == msg.from_user.id)).fetchall():
                ss.execute(insert(User).values([(msg.from_user.id, False)]))
                ss.commit()
        return ss.execute(select(User).where(User.id == msg.from_user.id)).fetchone()[0]
