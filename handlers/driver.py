from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from datetime import datetime
import logging

from states.driver import DriverStates
from keyboards.driver import driver_menu
from texts.driver import TEXTS
from data.storage import DRIVERS

router = Router()
logger = logging.getLogger(__name__)


# 🚗 Старт регистрации водителя
@router.message(F.text == "🧑‍✈️ Водитель")
async def driver_registration(message: types.Message, state: FSMContext):
    await message.answer(TEXTS.REGISTRATION_PROMPT)
    await state.set_state(DriverStates.waiting_for_car_model)


# 🚘 Получение модели авто
@router.message(DriverStates.waiting_for_car_model)
async def get_car_model(message: types.Message, state: FSMContext):
    car_model = message.text.strip()
    if not car_model:
        await message.answer(TEXTS.INVALID_MODEL)
        return

    await state.update_data(car_model=car_model)
    await message.answer(TEXTS.ENTER_CAR_NUMBER)
    await state.set_state(DriverStates.waiting_for_car_number)


# 🚕 Получение номера авто
@router.message(DriverStates.waiting_for_car_number)
async def get_car_number(message: types.Message, state: FSMContext):
    car_number = message.text.strip().upper()
    if not car_number:
        await message.answer(TEXTS.INVALID_NUMBER)
        return

    data = await state.update_data(car_number=car_number)
    driver_id = message.from_user.id

    DRIVERS[driver_id] = {
        "car_model": data.get("car_model", "Не указано"),
        "car_number": car_number,
        "online": False,
        "registered_at": datetime.now().isoformat()
    }

    logger.info(f"Водитель {driver_id} зарегистрирован: {DRIVERS[driver_id]}")
    await message.answer(TEXTS.SUCCESS_REGISTRATION, reply_markup=driver_menu())
    await state.set_state(DriverStates.registered)


# 🔛 Переход в режим "онлайн"
@router.message(F.text == "🔛 Онлайн")
async def go_online(message: types.Message):
    driver_id = message.from_user.id
    driver = DRIVERS.get(driver_id)

    if not driver:
        await message.answer(TEXTS.NOT_REGISTERED, reply_markup=driver_menu())
        return

    if driver["online"]:
        await message.answer(TEXTS.ALREADY_ONLINE, reply_markup=driver_menu())
        return

    driver["online"] = True
    logger.info(f"Водитель {driver_id} теперь онлайн")
    await message.answer(TEXTS.NOW_ONLINE, reply_markup=driver_menu())


# 🔴 Переход в режим "офлайн"
@router.message(F.text == "🔴 Офлайн")
async def go_offline(message: types.Message):
    driver_id = message.from_user.id
    driver = DRIVERS.get(driver_id)

    if not driver:
        await message.answer(TEXTS.NOT_REGISTERED, reply_markup=driver_menu())
        return

    if not driver["online"]:
        await message.answer(TEXTS.ALREADY_OFFLINE, reply_markup=driver_menu())
        return

    driver["online"] = False
    logger.info(f"Водитель {driver_id} теперь офлайн")
    await message.answer(TEXTS.NOW_OFFLINE, reply_markup=driver_menu())