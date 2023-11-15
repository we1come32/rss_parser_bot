from urllib.parse import urlsplit

from aiogram import Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from cachetools.func import ttl_cache
from loguru import logger
from sqlalchemy import insert, select, func
from sqlalchemy.orm import Session

from config import TG_ADMIN_ID
from models import engine, Service, User, Subscription, Subscribe, Message as MessageUtil, Language
from utils.chat.filters import DevBotFilter, IsAdminFilter
from utils.decorators.get_user import get_user_from_message


dp = Dispatcher()


@dp.message(DevBotFilter(), CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик для команды /start
    """
    user: User | None = get_user_from_message(message)
    if not user:  # == None
        return
    await message.answer(MessageUtil.get_translate("Привет!", user.language_id))


@dp.message(DevBotFilter(), Command(commands=["add_rss", "add"]))
async def add_rss(message: Message):
    """
    Обработчик для подписки на новости
    """
    user = get_user_from_message(message)
    # Если сообщение не от пользователя, игнорируем
    if not user:
        return
    msg_text = message.text.split()
    result_message = "Please, send rss-link with this command."
    kwargs = {}
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

                    # Get or create user subscription
                    rq = select(Subscribe).where(Subscribe.subscription_id == sub.id)
                    if not(ss.execute(rq).fetchall()):
                        ss.execute(insert(Subscribe).values(subscription_id=sub.id, user_id=message.from_user.id))
                    ss.commit()
                    result_message = "You subscribe onto {url!r}."
                    kwargs = dict(url=url.geturl())
                else:
                    result_message = "Service from url {url!r} is not allowed."
                    kwargs = dict(url=service.base_url)
            else:
                result_message = "Unknown service or service is not allowed."

    # Отвечаем переведённым сообщением с нужными аргументами
    await message.reply(MessageUtil.get_translate(result_message, user.language_id).format(**kwargs))


@ttl_cache(ttl=30)
def get_language_statistic() -> dict[str, int]:
    req = select(
        Language.name,
        func.count(MessageUtil.language_id),
    ).where(
        MessageUtil.language_id == Language.id,
    ).group_by(Language.name)

    with Session(engine) as ss:
        en_count = 0
        result = {}
        for language_name, value in sorted(ss.execute(req), key=lambda tmp: tmp[1], reverse=True):
            if language_name == "English":
                en_count = value
                continue
            result[language_name] = int(value / en_count * 100)
    return result


@dp.message(IsAdminFilter(), Command(commands=["statistic"]))
async def statistic(message: Message):
    user: User = get_user_from_message(message)
    result = ""
    for number, (language, percent) in enumerate(get_language_statistic().items()):
        result += f"{number+1}) {language} - {percent}%\n"
    await message.reply(MessageUtil.get_translate("Statistic:\n\n{values}", user.language_id).format(values=result))


@dp.message(DevBotFilter(), Command(commands=["allow"]), F.from_user.id.in_([TG_ADMIN_ID]))
async def allow_service(message: Message):
    pass
