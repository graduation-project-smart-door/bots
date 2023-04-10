import logging

from aiogram import Bot

from aiohttp.web_request import Request
from aiohttp.web_response import json_response


logger = logging.getLogger(__name__)

MESSAGES = {
    "day": "Желает всем хорошего дня 🌝",
    "evening": "Желает всем хорошего вечера 🌚",
}

async def send_notification(request: Request):
    data = await request.post()
    bot: Bot = request.app["bot"]
    
    chat_id: int = request.app['chat_id']

    first_name = data['first_name']
    last_name = data['last_name']
    text = MESSAGES[data['type']]

    await bot.send_message(chat_id=chat_id, text=f'{first_name} {last_name} {text}')

    return json_response({"ok": True})
