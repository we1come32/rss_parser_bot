from datetime import datetime
from typing import Tuple

from loguru import logger
from sqlalchemy import ForeignKey, MetaData, create_engine, select, insert
from sqlalchemy import String, INT, Boolean, BIGINT, DateTime
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from config import DB_USER, DB_NAME, DB_PASS, DB_HOST, DB_PORT, DEBUG


metadata = MetaData()
engine = create_engine(
    "postgresql+psycopg2://{user}:{password}@{url}:{port}/{db_name}".format(
        user=DB_USER,
        password=DB_PASS,
        url=DB_HOST,
        port=DB_PORT,
        db_name=DB_NAME
    ),
    echo=DEBUG
)

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(INT(), primary_key=True)
    blocked: Mapped[bool] = mapped_column(Boolean(), default=False)
    language: Mapped[str] = mapped_column(String(8), default="en", nullable=True)

    subscriptions: Mapped["Subscribe"] = relationship()

    def __repr__(self):
        return f"<User id={self.id} blocked={self.blocked}>"


class Service(Base):
    """
    Таблица с разрешёнными сервисами
    """
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(INT(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20))
    base_url: Mapped[str] = mapped_column(String())
    activated: Mapped[bool] = mapped_column(Boolean(), default=False)

    def __repr__(self):
        return f"<Service id={self.id} name={self.name} url={self.base_url}>"


class Subscription(Base):
    """
    RSS-ссылка на подписку о новостях
    """
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(BIGINT(), primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String(length=150))

    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))


class Subscribe(Base):
    """
    Подписка пользователей на определённые RSS-ссылки
    """
    __tablename__ = "user_subscriptions"

    id: Mapped[int] = mapped_column(INT(), primary_key=True, autoincrement=True)

    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Task(Base):
    """
    Задачи с сервисов
    """
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(BIGINT(), primary_key=True, autoincrement=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(600))
    url: Mapped[str] = mapped_column(String(50))
    themes: Mapped[str] = mapped_column(String(50))
    price: Mapped[str] = mapped_column(String(50))
    limit_time: Mapped[str] = mapped_column(String(50))
    publish_date: Mapped[str] = mapped_column(String(50))
    author: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"<Task id={self.id}, platform={self.service_id}>"


class TaskViewStatus(Base):
    __tablename__ = "task_views"

    id: Mapped[int] = mapped_column(BIGINT(), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BIGINT(), primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(String(512))
    language: Mapped[str] = mapped_column(String(8))
    original_id: Mapped[str] = mapped_column(ForeignKey("messages.id"))

    last_usage: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def translate(self, lang: str) -> Tuple[str, bool]:
        with Session(engine) as ss:
            req = select(Message).values(original_id=self.id, language=lang)
            res = ss.execute(req).fetchall()
            if res:
                return res[0][0].message, True
        return "", False

    @staticmethod
    def get_translate(message: str, lang: str = "en"):
        if lang == "en":
            return message
        req = select(Message).where(Message.message == message)
        translated = False
        with Session(engine) as ss:
            msgs = ss.execute(req).fetchall()
            if msgs:
                # Если такое сообщение было найдено в программе раньше, то ищем для него перевод в базе
                msg: Message = msgs[0][0]
                message, translated = msg.translate(lang)
            else:
                # Иначе создаём данный текст в базе данных
                req = insert(Message).values(message=message, language="en",
                                             original_id=None, last_usage=datetime.now())
                ss.execute(req)
            ss.commit()
        if not translated:
            logger.warning("Message \"{msg}\" is not translated into \"{lang}\" language", msg=message, lang=lang)
        return message
