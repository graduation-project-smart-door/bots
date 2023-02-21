import asyncio
import logging
import nest_asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot.config import Config, load_config
from tgbot.handlers.door.router import door_router
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.bot import BotMiddleware

logger = logging.getLogger(__name__)


def register_all_handlers(dp):
    dp.include_router(door_router)


def register_all_middlewares(dp: Dispatcher, config: Config, bot: Bot):
    config_middleware = ConfigMiddleware(config)
    bot_middleware = BotMiddleware(bot)

    dp.update.middleware(config_middleware)
    dp.update.middleware(bot_middleware)


async def main():
    nest_asyncio.apply()

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s]'
        '- %(name)s - %(message)s'
        )

    logger.info("Starting bot")

    config = load_config(".env")

    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    dp = Dispatcher(storage=storage)

    register_all_handlers(dp)
    register_all_middlewares(dp, config, bot)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
