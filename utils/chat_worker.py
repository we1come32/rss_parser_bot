from typing import Any, Union, Dict
from urllib.parse import urlsplit

from aiogram import Dispatcher, F
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.types import Message
from loguru import logger
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from config import TG_ADMIN_ID
from models import engine, Service, User, Subscription, Subscribe


class DevBotFilter(BaseFilter):
    async def __call__(self, *args: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        pass


dp = Dispatcher()


@dp.message(DevBotFilter(), CommandStart())
async def command_start_handler(message: Message) -> None:
    if not message.from_user:
        return
    with Session(engine) as ss:
        if not ss.execute(select(User).where(User.id == message.from_user.id)).fetchall():
            ss.execute(insert(User).values([(message.from_user.id, False)]))
            ss.commit()
    await message.answer(f"Привет!")


@dp.message(DevBotFilter(), Command(commands=["add_rss", "add"]))
async def add_rss(message: Message):
    msg_text = message.text.split()
    result_message = "Please, send rss-link with this command."
    if len(msg_text) == 2:
        url = urlsplit(msg_text[1])
        with Session(engine) as ss:
            rq = select(Service).where(
                Service.base_url.contains(url.netloc)
            )
            if url.netloc and (services := ss.execute(rq).fetchall()):
                service: Service = services[0][0]
                if service.activated:

                    # Get or create url subscription
                    rq = select(Subscription).where(Subscription.url == url.geturl())
                    if (subs := ss.execute(rq).fetchall()):
                        sub = subs[0][0]
                    else:
                        # Creating
                        ss.execute(insert(Subscription).values(url=url.geturl(), service_id=service.id))
                        # Get sub.id from db
                        sub = ss.execute(select(Subscription).where(Subscription.url == url.geturl())).fetchall()[0][0]
                    logger.debug(sub)

                    # Get or create user subscription
                    rq = select(Subscribe).where(Subscribe.subscription_id == sub.id)
                    if not(ss.execute(rq).fetchall()):
                        ss.execute(insert(Subscribe).values(subscription_id=sub.id, user_id=message.from_user.id))
                    ss.commit()
                    result_message = f"Hello, its working! You subscribe onto {url.geturl()!r}."
                else:
                    result_message = f"Service from url {service.base_url} is not allowed."
            else:
                result_message = "Unknown service or service is not allowed."
    await message.reply(result_message)


@dp.message(Command(commands=["allow"]), F.from_user.id.in_([TG_ADMIN_ID]))
async def allow_service(message: Message):
    pass
