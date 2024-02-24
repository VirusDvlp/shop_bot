from aiogram.fsm.state import State, StatesGroup



class AddGoodFSM(StatesGroup):
    nameState = State()
    descrState = State()
    priceState = State()
    imageState = State()
    categoryState = State()
