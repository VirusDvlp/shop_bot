from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext

import aiogram.filters as f

from FSM import UserRegistrationFSM
from config import db
from filters import TextFilter

import keyboards as kb



async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    if db.check_user_exist(message.from_user.id):
        await message.answer(
            'Открыто главное меню пользователя',
            reply_markup=kb.main_user_kb
        )
    else:
        await state.set_state(UserRegistrationFSM.nameState)
        await message.answer('Добро пожаловать! Вам необходимо зарегистрироваться. Введите своё ФИО')


async def register_user(message: types.Message, state: FSMContext):
    await state.clear()
    db.add_user(message.from_user.id, message.from_user.username, message.text)
    await message.answer('Вы успешно зарегистрировались!', reply_markup=kb.main_user_kb)


async def about(message: types.Message):
    await message.answer('О магазине')


def register_main_user_handlers(dp: Dispatcher) -> None:
    dp.message.register(start_cmd, f.CommandStart(), f.StateFilter('*'))
    dp.message.register(register_user, f.StateFilter(UserRegistrationFSM.nameState))
    dp.message.register(about, TextFilter('О нас'))
