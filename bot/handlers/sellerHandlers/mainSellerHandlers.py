from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
import aiogram.filters as f

from aiofiles import open as o

from json import loads

from filters import TextFilter, CheckSellerFilter
from config import SELLERS_ID

import keyboards as kb



async def seller_start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    async with o('sellers_data.json') as file:
        data = loads(await file.read())
    if data['cur_seller'] == message.from_user.id:
        await message.answer(
            'Открыто главное меню продавца',
            reply_markup=kb.main_seller_kb
        )
    else:
        await message.answer('Чтобы начать работу возьмите смену, нажав кнопку ниже:', reply_markup=kb.get_shift_kb)


async def return_to_seller_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Открыто главное меню продавца',
        reply_markup=kb.main_seller_kb
    )


def register_main_seller_handlers(dp: Dispatcher) -> None:
    dp.message.register(seller_start_cmd, f.CommandStart(), f.StateFilter('*'), lambda mess: mess.from_user.id in SELLERS_ID)
    dp.message.register(return_to_seller_menu, TextFilter('ВЕРНУТЬСЯ В МЕНЮ'), f.StateFilter('*'), CheckSellerFilter())
