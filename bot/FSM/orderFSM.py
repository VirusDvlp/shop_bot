from aiogram.fsm.state import State, StatesGroup


class OrderRequestFSM(StatesGroup):
    gettingTypeState = State()
    whereState = State()


class CancelRequestFSM(StatesGroup):
    messageState = State()
    messageOrderState = State()


class OrderBuyFSM(StatesGroup):
    payTypeState = State()
    paySysState = State()
    payState = State()
