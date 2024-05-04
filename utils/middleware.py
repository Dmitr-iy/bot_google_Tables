from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.flags import get_flag
from aiogram.utils.chat_action import ChatActionSender


class SheetIdMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

        self.sheet_id = None
        self.work_sheet = None

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ):
        sheet_id = self.sheet_id
        work_sheet = self.work_sheet
        data["sheet_id"] = sheet_id
        data["work_sheet"] = work_sheet
        result = await handler(event, data)
        return result


sheet_id_middleware = SheetIdMiddleware()


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        long_operation_type = get_flag(data, "long_operation")

        # Если такого флага на хэндлере нет
        if not long_operation_type:
            return await handler(event, data)

        # Если флаг есть
        async with ChatActionSender(
                action=long_operation_type,
                chat_id=event.chat.id
        ):
            return await handler(event, data)
