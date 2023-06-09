from copy import copy
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, types
from aiogram.types import TelegramObject
from tgbot.language.translator import Translator


class TranslatorMD(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        new_data = copy(data)
        translator: Translator = new_data['translator']
        new_data['translator'] = translator(language=event.from_user.language_code)
        return await handler(event, new_data)


class L10nMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        from_user: types.User = event.from_user
        # user_data = await User.by_user_id(from_user.id) or await User.set_user(from_user)

        # lang = user_data.lang or from_user.language_code
        # data["l10n"] = data["fluent"].get_translator_by_locale(lang)

        return await handler(event, data)
