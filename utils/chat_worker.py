from urllib.parse import urlsplit

from aiogram import Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from loguru import logger
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from models import engine, Service

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет!")


@dp.message(Command(commands=["add_rss", "add"]))
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
                    result_message = f"Hello, its working! This service is {service.name!r}"
                else:
                    result_message = f"Service from url {service.base_url} is not allowed."
            else:
                result_message = "Unknown service or service is not allowed."
    await message.reply(result_message)
