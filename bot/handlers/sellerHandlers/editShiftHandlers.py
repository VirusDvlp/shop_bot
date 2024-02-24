from aiogram import types, Dispatcher

from aiofiles import open as aiopen

from json import loads, dumps

from filters import TextFilter, CheckSellerFilter
from config import SELLERS_ID
import keyboards as kb


async def set_shift(message: types.Message):
    async with aiopen('sellers_data.json') as file:
        data = loads(await file.read())
    if data['cur_seller'] == 0:
        data['cur_seller'] = message.from_user.id
        async with aiopen('sellers_data.json', 'w') as file:
            await file.write(dumps(data, ensure_ascii=False, indent=4))
        await message.answer('Вы успешно приняли смену', reply_markup=kb.main_seller_kb)
    else:
        await message.answer('Смена занята другим продавцом')


async def unset_shift(message: types.Message):
    async with aiopen('sellers_data.json') as file:
        data = loads(await file.read())
    if data['cur_seller'] == message.from_user.id:
        data['cur_seller'] = 0
        async with aiopen('sellers_data.json', 'w') as file:
            await file.write(dumps(data, ensure_ascii=False, indent=4))
        await message.answer('Вы успешно сдали смену', reply_markup=kb.get_shift_kb)
    else:
        await message.answer('В данный момент вы не в смене')


def register_edit_shift_handlers(dp: Dispatcher) -> None:
    dp.message.register(set_shift, TextFilter('Взять смену'), lambda mess: mess.from_user.id in SELLERS_ID)
    dp.message.register(unset_shift, TextFilter('Сдать смену'), CheckSellerFilter())
