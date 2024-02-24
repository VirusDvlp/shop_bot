from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID


class CheckAdminFilter:


    def __call__(self, message: Message, CallbackQuery) -> bool:
        return message.from_user.id == ADMIN_ID
