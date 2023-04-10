import logging

from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from tgbot.handlers.door.service import create_user

from tgbot.misc.states import CreateUser



door_router = Router()
logger = logging.getLogger(__name__)


@door_router.message(Command(commands=["start"]))
async def command_start_handler(message: Message, state: FSMContext):
    await message.answer(
        f"Здравствуйте! Пожалуйста, отправьте видео"
    )

    await state.set_state(CreateUser.video)


@door_router.message(CreateUser.video, F.video)
async def get_video(message: Message, state: FSMContext) -> None:
    await state.update_data(file_id=message.video.file_id)
    
    await message.answer("Отлично! Теперь введите имя и фамилию через пробел с большой буквы\nПример: Вася Пупкин")
    await state.set_state(CreateUser.full_name)


@door_router.message(CreateUser.video, ~F.video)
async def get_not_video(message: Message, state: FSMContext) -> None:
    await message.answer("Извините, но мы требует именно видео. Попробуйте ещё разок")


@door_router.message(CreateUser.full_name)
async def get_full_name(message: Message, state: FSMContext):    
    full_name = message.text
    
    full_name_list = full_name.split(' ')
    if len(full_name_list) != 2:
        await message.answer("Ты дурачок? Попробуй ещё раз")

        return
    
    first_name, last_name = full_name_list
    
    await state.update_data(first_name=first_name)
    await state.update_data(last_name=last_name)

    await message.answer("Введите должность:")
    await state.set_state(CreateUser.position)


@door_router.message(CreateUser.position)
async def get_position(message: Message, state: FSMContext, bot: Bot) -> None:
    position = message.text

    file_id: str = (await state.get_data())['file_id']

    data: dict = await state.get_data()
    
    url = "http://127.0.0.1:8001/video"
    
    video = await bot.get_file(file_id)

    create_user(data['first_name'], data['last_name'], position, video, url)
    
    await message.answer("Пользователь успешно создан")
    await state.clear()
