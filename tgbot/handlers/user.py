from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart, Command, Text, StateFilter
from aiogram.fsm.storage.redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tgbot.models.user import User
from tgbot.language.translator import LocalizedTranslator
# from tgbot.config import redis

router = Router()


@router.message(CommandStart())
async def start_command(
    message: Message, 
    db: AsyncSession,
    translator: LocalizedTranslator,
    cache: Redis,
    ):
    user = message.from_user
    await cache.set(name=user.id, value='414141')
    to_db = select(User).where(User.telega_id == user.id)
    current_user = await db.scalar(to_db)
    if current_user is None:
        current_user = User(
            telega_id=user.id,
            username=user.username,
            first_name=user.first_name,
            language_code=user.language_code,
            is_bot=user.is_bot,
        )
        db.add(current_user), await db.commit()
    print(await cache.get(name=user.id))
    await message.answer(
        text=translator.get(key='test'),
        # reply_markup=keyword
   )

