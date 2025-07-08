from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from states.user import UserStates
from keyboards.default import main_menu, cancel_kb, from_method_kb
from keyboards.inline import driver_request_kb
from data.storage import USERS, PENDING_ORDERS, DRIVERS
from texts.user import TEXTS

import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def auto_register_on_start(message: types.Message, state: FSMContext):
    user = message.from_user
    USERS[user.id] = {
        "id": user.id,
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
        "username": user.username or ""
    }

    logger.info(f"Пользователь {user.id} зарегистрирован автоматически: {USERS[user.id]}")
    await message.answer(TEXTS.REG_SUCCESS, reply_markup=main_menu())
    await state.clear()


@router.message(F.text == "🚖 Заказать такси")
async def start_order(message: types.Message, state: FSMContext):
    await message.answer(TEXTS.ENTER_FROM_METHOD, reply_markup=from_method_kb())
    await state.set_state(UserStates.choosing_from_method)


@router.message(F.location)
async def handle_location(message: types.Message, state: FSMContext):
    location = message.location
    if not location:
        await message.answer(TEXTS.INVALID_ADDRESS, reply_markup=from_method_kb())
        return

    address = f"{location.latitude}, {location.longitude}"
    await state.update_data(from_address=address)
    await message.answer(TEXTS.WAITING_DRIVER, reply_markup=main_menu())

    user_id = message.from_user.id
    PENDING_ORDERS[user_id] = await state.get_data()
    logger.info(f"Пользователь {user_id} отправил заказ с координат: {address}")

    for driver_id, driver in DRIVERS.items():
        if driver.get("online"):
            try:
                await message.bot.send_message(
                    driver_id,
                    TEXTS.NEW_ORDER.format(
                        from_addr=address,
                        to_addr="(не указано)"
                    ),
                    reply_markup=driver_request_kb(user_id)
                )
            except Exception as e:
                logger.warning(f"Ошибка при отправке водителю {driver_id}: {e}")

    await state.clear()


@router.message(F.text == "✍️ Ввести адрес")
async def enter_address_by_text(message: types.Message, state: FSMContext):
    await message.answer(TEXTS.ENTER_FROM_ADDRESS, reply_markup=cancel_kb())
    await state.set_state(UserStates.entering_from_address)


@router.message(UserStates.entering_from_address)
async def handle_text_address(message: types.Message, state: FSMContext):
    address = message.text.strip()
    if not address:
        await message.answer(TEXTS.INVALID_ADDRESS, reply_markup=cancel_kb())
        return

    await state.update_data(from_address=address)
    await message.answer(TEXTS.WAITING_DRIVER, reply_markup=main_menu())

    user_id = message.from_user.id
    PENDING_ORDERS[user_id] = await state.get_data()
    logger.info(f"Пользователь {user_id} ввёл адрес: {address}")

    for driver_id, driver in DRIVERS.items():
        if driver.get("online"):
            try:
                await message.bot.send_message(
                    driver_id,
                    TEXTS.NEW_ORDER.format(
                        from_addr=address,
                        to_addr="(не указано)"
                    ),
                    reply_markup=driver_request_kb(user_id)
                )
            except Exception as e:
                logger.warning(f"Ошибка при отправке водителю {driver_id}: {e}")

    await state.clear()


@router.message(F.text == "❌ Отмена")
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(TEXTS.CANCELLED, reply_markup=main_menu())