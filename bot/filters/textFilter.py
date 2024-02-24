from aiogram.types import Message, CallbackQuery


from typing import Any


class TextFilter:
    def __init__(self, text: str) -> None:
        self.text = text
    

    def __call__(self, data: Message | CallbackQuery) -> Any:
        if isinstance(data, Message):
            return data.text == self.text
        elif isinstance(data, CallbackQuery):
            return data.data == self.text
        else:
            raise TypeError("Невверное использование фильтра")
