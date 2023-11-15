from typing import Any, Union, Dict

from aiogram.filters import BaseFilter
from aiogram.types import Message

from config import DEBUG
from models import User
from utils.decorators.get_user import get_user_from_message


class DevBotFilter(BaseFilter):
    """
    Фильтр на DEBUG-режим. Бот доступен в этом режиме только для администраторов
    """
    async def __call__(self, message: Message, *args, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        user: User = get_user_from_message(message)
        if not user:  # == None
            return False  # Ignore this command
        return not DEBUG or bool(user.is_admin)


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        user: User = get_user_from_message(message)
        if not user:  # == None
            return False  # Ignore this command
        return bool(user.is_admin)
