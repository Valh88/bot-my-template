import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis
from tgbot.handlers import user, echo
from tgbot.config import config, Config
from tgbot.models.database import create_db_session
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.database import DbMiddleware
from tgbot.middlewares.throttilng import ThrottlingMiddleware
from tgbot.middlewares.I10n import TranslatorMD
from tgbot.keyboards.main_menu import main_menu
from tgbot.language.translator import Translator
from tgbot.config import redis
logger = logging.getLogger(__name__)


def register_global_middleware(dp: Dispatcher, config: Config, session_pool):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))
    
    dp.message.outer_middleware(DbMiddleware(session_pool))
    dp.callback_query.outer_middleware(DbMiddleware(session_pool))

    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())

    dp.message.middleware(TranslatorMD())
    dp.callback_query.middleware(TranslatorMD())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    await main_menu(bot)

    if config.tg_bot.use_redis:
        storage: RedisStorage = RedisStorage(redis=redis)
    else:
        storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    session_pool = await create_db_session(config)
    register_global_middleware(dp, config, session_pool)

    dp.include_router(user.router)
    dp.include_router(echo.router)

    # start
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            translator=Translator()
            )
    finally:
        await dp.storage.close()
        # await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
