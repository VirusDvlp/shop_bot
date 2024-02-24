from aiogram import types, Dispatcher
from aiogram.filters import StateFilter



async def answer_callback(callback: types.CallbackQuery):
    await callback.answer()



def register_default_handlers(dp: Dispatcher) -> None:
    dp.callback_query.register(answer_callback, StateFilter('*'))
