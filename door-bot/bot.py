import asyncio
import logging
import nest_asyncio

from aiohttp.web import run_app
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from tgbot.config import Config, load_config
from tgbot.handlers.door.router import door_router
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.handlers.users.service import send_notification


logger = logging.getLogger(__name__)


def register_all_handlers(dp):
    dp.include_router(door_router)

def register_all_middlewares(dp: Dispatcher, config: Config):
    config_middleware = ConfigMiddleware(config)

    dp.update.middleware(config_middleware)


async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{base_url}/webhook")


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
    dp["base_url"] = 'https://c94d-2a03-d000-6506-a6db-dc3-28c1-e20-9796.ngrok-free.app'
    dp.startup.register(on_startup)

    app = Application()
    app['bot'] = bot
    app['chat_id'] = config.chat_id

    register_all_handlers(dp)

    app.router.add_post("/recognize", send_notification)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    run_app(app, host="127.0.0.1", port=8087)

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
