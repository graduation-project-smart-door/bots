import logging
from datetime import datetime

from aiogram import Bot

from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from requests import Response

def get_time_of_day(time: int) -> str:
    if time < 12:
        return "morning"
    elif time < 16:
        return "day"
    elif time < 19:
        return "evening"

    return "night"


MESSAGES = {
    "morninig": "желает всем хорошего утра 🌅",
    "day": "желает всем хорошего дня 🌝",
    "evening": "желает всем хорошего вечера 🎇",
    "night": "желает всем хорошей ночи 🌚",
}

async def send_notification(request: Request) -> Response:
    now = datetime.now()

    data = await request.json()
    bot: Bot = request.app["bot"]
    
    chat_id: int = request.app['chat_id']

    first_name = data['first_name']
    last_name = data['last_name']
    text = MESSAGES[get_time_of_day(now.hour)]

    await bot.send_message(chat_id=chat_id, text=f'{first_name} {last_name} {text}')

    return json_response({"ok": True})
