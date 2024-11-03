from aiogram.fsm.state import State, StatesGroup


class LogState(StatesGroup):
    view = State()
    
    login = State()
    email = State()
    code = State()
    passw = State()

    phone = State()
    passw_phone = State()
    code_ph = State()
