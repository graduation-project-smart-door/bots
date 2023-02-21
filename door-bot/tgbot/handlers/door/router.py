import logging
import requests

from aiogram import Router, types, Bot
from aiogram.filters import Command


door_router = Router()
logger = logging.getLogger(__name__)

@door_router.message(Command(commands=["start"]))
async def command_start_handler(message: types.Message) -> None:
    await message.answer(f'Hello, {message.chat.first_name} {message.chat.last_name}\nYour username: <strong>{message.chat.username}</strong>')


@door_router.message()
async def save_video(message: types.Message, bot: Bot) -> None:
    # TODO: Добавить обработку неправильных расширений. Поддерживается только mp4
    # TODO: Вынести baseUrl в .env
    file = await bot.get_file(message.video.file_id)
    file_path = file.file_path

    url = 'http://ml-learning:8081/video'
    logger.info(f'send from bot to {url}')
    requests.post(url, json={ "file_path": file_path }, verify=False)
