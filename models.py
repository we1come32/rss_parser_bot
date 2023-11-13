from sqlalchemy import ForeignKey, MetaData, create_engine
from sqlalchemy import String, INT, Boolean, BIGINT
from sqlalchemy.orm import DeclarativeBase, declarative_base
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
    blocked: Mapped[bool] = mapped_column(Boolean())

    subscriptions: Mapped["Subscribe"] = relationship()#back_populates="addresses")

    def __repr__(self):
        return f"<User id={self.id}>"


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
