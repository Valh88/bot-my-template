from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart, Command, Text, StateFilter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tgbot.models.user import User
from tgbot.language.translator import LocalizedTranslator

router = Router()


@router.message(CommandStart())
async def start_command(
    message: Message, 
    session: AsyncSession,
    translator: LocalizedTranslator,
    ):
    user = message.from_user
    to_db = select(User).where(User.telega_id == user.id)
    current_user = await session.scalar(to_db)
    if current_user is None:
        current_user = User(
            telega_id=user.id,
            username=user.username,
            first_name=user.first_name,
            language_code=user.language_code,
            is_bot=user.is_bot,
        )
        session.add(current_user), await session.commit()

    await message.answer(
        text=translator.get(key='test'),
        # reply_markup=keyword
   )

