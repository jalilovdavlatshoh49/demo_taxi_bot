from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    choosing_from_method = State()
    entering_from_address = State()