from aiogram.types import Message, CallbackQuery


from typing import Any


class StartsWithFilter:
    def __init__(self, startswith: str) -> None:
        self.startswith = startswith
    

    def __call__(self, data: Message | CallbackQuery) -> Any:
        if isinstance(data, Message):
            return data.text.startswith(self.startswith)
        elif isinstance(data, CallbackQuery):
            return data.data.startswith(self.startswith)
        else:
            raise TypeError("Невверное использование фильтра")