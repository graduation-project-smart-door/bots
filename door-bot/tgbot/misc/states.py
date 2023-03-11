from aiogram.fsm.state import State, StatesGroup


class CreateUser(StatesGroup):
    full_name = State()
    video = State()
