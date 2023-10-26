from sqlalchemy import ForeignKey, MetaData
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


metadata = MetaData()

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    blocked: Mapped[bool] = mapped_column(Boolean())

    subscriptions: Mapped["Subscribe"] = relationship(back_populates="addresses")

    def __repr__(self):
        return f"<User id={self.id}>"


class Services(Base):
    """
    Таблица с разрешёнными сервисами
    """
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
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

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    url: Mapped[str] = mapped_column(String(length=150))

    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))


class Subscribe(Base):
    """
    Подписка пользователей на определённые RSS-ссылки
    """
    __tablename__ = "user_subscriptions"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)

    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Task(Base):
    """
    Задачи с сервисов
    """
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(600))
    url: Mapped[str] = mapped_column(String(50))
    themes: Mapped[str] = mapped_column(String(50))
    price: Mapped[str] = mapped_column(String(50))
    limit_time: Mapped[str] = mapped_column(String(50))
    publish_date: Mapped[str] = mapped_column(String(50))
    author: Mapped[str] = mapped_column(String(50))


class TaskViewStatus(Base):
    __tablename__ = "task_views"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
