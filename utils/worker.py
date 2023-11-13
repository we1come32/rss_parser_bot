from random import randint

from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import sleep
from sqlalchemy import select
from sqlalchemy.orm import Session

from logger import logger
from models import Subscribe, User
from bot import bot
from messages import new_task_message, short_new_task_message
from models import Subscription, Service, engine
from utils.parser import parse


async def run() -> None:
    while True:
        with Session(engine) as session:
            subscribes = select(Subscription, Service).join(Service).where(
                Service.activated == True  # Что сервис активен в беке
            )
            for (sub, service) in session.execute(subscribes):
                sub: Subscription
                service: Service

                async for task in parse(url=sub.url):
                    logger.success("New task! Platform={platform_name} {task}", task=task,
                                   platform_name=service.name)
                    message_cfg = dict(
                        platform=service.name,
                        title=task.title,
                        description=task.description,
                        themes=", ".join(task.tags),
                        published_date=task.published_date,
                    )
                    message = new_task_message.format(**message_cfg)
                    if len(message) > 4096:
                        message = short_new_task_message.format(**message_cfg)

                    # Рассылка
                    req = select(Subscribe).join(User).where(
                        User.blocked == False,
                        Subscribe.subscription_id == sub.id
                    )
                    for (user, ) in session.execute(req):
                        user: Subscribe
                        try:
                            await bot.send_message(
                                user.user_id,
                                text=message,
                                parse_mode=ParseMode.HTML,
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                                   InlineKeyboardButton(text='Открыть задачу',
                                                        url=task.link)
                                ]])
                            )
                        except TelegramBadRequest:
                            logger.exception("Telegram invalid exception. Length: {length}\nMessage: {msg}",
                                             length=len(message), msg=message)
                await sleep(5)
            session.commit()
        await sleep(randint(90, 240))
