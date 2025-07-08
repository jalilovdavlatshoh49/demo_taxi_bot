from aiogram.fsm.state import State, StatesGroup

class DriverStates(StatesGroup):
    waiting_for_car_model = State()
    waiting_for_car_number = State()
    registered = State()