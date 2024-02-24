from aiogram import types, Dispatcher
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

from filters import CheckAdminFilter
import keyboards as kb



async def admin_start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Открыто главное меню администратор', reply_markup=kb.main_admin_kb)


def register_main_admin_handlers(dp: Dispatcher) -> None:
    dp.message.register(admin_start_cmd, CommandStart(), StateFilter('*'), CheckAdminFilter())
