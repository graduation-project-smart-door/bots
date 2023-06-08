from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    chat_id: int
    base_url: str
    host: str
    port: int
    backend_url: str
    frame_maker_url: str


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
        ),
        chat_id=env.int("CHAT_ID"),
        base_url=env.str("APP_BASE_URL"),
        host=env.str('HOST'),
        port=env.int('PORT'),
        backend_url=env.str('BACKEND_URL'),
        frame_maker_url=env.str('FRAME_MAKER_URL')
    )
