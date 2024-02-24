from aiogram.fsm.state import State, StatesGroup


class AskGoodDataFSM(StatesGroup):
    actionState = State()
    catState = State()
    goodState = State()
    dataState = State()
