import logging
import random

from aiogram import Bot

from tgbot.config import Config


MESSAGES = [
    "Доброе утро",
    "Good morning",
    "Bonjour",
    "おはよう",
    "早",
    "Guten Morgen",
    "Добрай раніцы",
    "Dzień dobry",
    "Доброго ранку",
    "Добро јутро",
    "Buenos días",
    "Buongiorno",
    "Қайырлы таң",
    "Godmorgen",
    "Dobré ráno",
]

logger = logging.getLogger(__name__)


async def send_good_morning(bot: Bot, config: Config):
    lang = random.choice(MESSAGES)

    await bot.send_message(chat_id=config.chat_id, text=lang)
