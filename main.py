from random import randint

from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from asyncio import run as run_async, sleep
from logger import logger


async def main() -> None:
    from bot import bot
    from config import admin_id, new_task_message, short_new_task_message
    from platforms.freelance_ru import Freelance_ru
    from platforms.fl_ru import Fl_ru

    platforms = [
        Fl_ru(),
        Freelance_ru(),
    ]

    while True:
        for platform in platforms:
            for task in platform.get_new_tasks():
                logger.success("New task! Platform={platform_name} {task}", task=task,
                               platform_name=platform.__class__.__name__)
                message = new_task_message.format(platform=platform.__class__.__name__, **task)
                if len(message) > 4096:
                    message = short_new_task_message.format(platform=platform.__class__.__name__, **task)
                try:
                    await bot.send_message(
                        admin_id,
                        text=message,
                        parse_mode=ParseMode.HTML,
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                           InlineKeyboardButton(text='Открыть задачу',
                                                url=task['href'])
                        ]])
                    )
                    await sleep(2)
                except TelegramBadRequest:
                    logger.exception("Telegram invalid exception. Length: {length}\nMessage: {msg}",
                                     length=len(message), msg=message)

        await sleep(randint(90, 240))


if __name__ == '__main__':
    load_dotenv()
    run_async(main())
