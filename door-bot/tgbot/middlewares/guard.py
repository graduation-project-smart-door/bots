import json
import logging
import os
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

logger = logging.getLogger(__name__)

WORKDIR = Path(__file__).parent.parent.parent.resolve()


class GuardMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        file = open(os.path.join(WORKDIR, 'access_ids.json'), "r")

        access_ids = json.load(file)

        if not event.from_user.id in access_ids:
          await event.answer('Дебил?')

          return

        return await handler(event, data)