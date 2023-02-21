from aiogram import BaseMiddleware, Bot


class BotMiddleware(BaseMiddleware):
    """Позволяет хендлерам получать bot"""

    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(self, handler, event, data):
        data['bot'] = self.bot
        return await handler(event, data)
