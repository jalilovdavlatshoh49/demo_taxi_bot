from aiogram import Router, types, F
from data.storage import ACTIVE_ORDERS, DRIVERS, PENDING_ORDERS
from keyboards.inline import rating_kb
import logging

router = Router()
logger = logging.getLogger(__name__)


# ✅ Водитель принимает заказ
@router.callback_query(F.data.startswith("accept_"))
async def accept_order(callback: types.CallbackQuery):
    try:
        user_id = int(callback.data.split("_")[1])
        driver_id = callback.from_user.id

        if user_id not in PENDING_ORDERS:
            await callback.message.answer("⚠️ Этот заказ больше неактивен.")
            return

        # Удаляем заказ из очереди
        order_data = PENDING_ORDERS.pop(user_id)

        # Помечаем активным заказом у водителя
        ACTIVE_ORDERS[driver_id] = user_id
        DRIVERS[driver_id]["online"] = False

        logger.info(f"Водитель {driver_id} принял заказ пользователя {user_id}")

        await callback.message.answer("🚗 Вы успешно приняли заказ.")
        await callback.bot.send_message(
            user_id,
            f"✅ Водитель принял ваш заказ!\n"
            f"🚘 Автомобиль: {DRIVERS[driver_id].get('car_model', 'Не указано')}\n"
            f"🔢 Номер: {DRIVERS[driver_id].get('car_number', 'Не указано')}",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="📍 Доставлен", callback_data="delivered")]
            ])
        )
    except Exception as e:
        logger.error(f"[accept_order] Ошибка: {e}")
        await callback.message.answer("❌ Произошла ошибка при принятии заказа.")


# ❌ Водитель отклоняет заказ
@router.callback_query(F.data.startswith("reject_"))
async def reject_order(callback: types.CallbackQuery):
    try:
        user_id = int(callback.data.split("_")[1])
        driver_id = callback.from_user.id

        await callback.message.answer("🚫 Вы отклонили заказ.")
        await callback.bot.send_message(user_id, "❌ К сожалению, водитель отклонил ваш заказ.")

        logger.info(f"Водитель {driver_id} отклонил заказ от пользователя {user_id}")
    except Exception as e:
        logger.error(f"[reject_order] Ошибка: {e}")
        await callback.message.answer("❌ Ошибка при отклонении заказа.")


# 📍 Отметка "доставлен"
@router.callback_query(F.data == "delivered")
async def mark_delivered(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id
        found = False

        for driver_id, uid in list(ACTIVE_ORDERS.items()):
            if uid == user_id:
                del ACTIVE_ORDERS[driver_id]
                DRIVERS[driver_id]["online"] = True

                await callback.bot.send_message(
                    user_id,
                    "🙏 Спасибо за поездку! Пожалуйста, оцените водителя:",
                    reply_markup=rating_kb()
                )

                logger.info(f"Пользователь {user_id} отметил доставку. Водитель {driver_id} снова в сети.")
                found = True
                break

        if not found:
            await callback.message.answer("⚠️ Доставленный заказ не найден.")
    except Exception as e:
        logger.error(f"[mark_delivered] Ошибка: {e}")
        await callback.message.answer("❌ Ошибка при отметке доставки.")


# ⭐ Обработка оценки водителя
@router.callback_query(F.data.startswith("rate_"))
async def handle_rating(callback: types.CallbackQuery):
    try:
        rating = callback.data.split("_")[1]
        await callback.message.answer(f"⭐ Вы поставили оценку: {rating}/5. Спасибо!")
        logger.info(f"Пользователь {callback.from_user.id} поставил оценку {rating}")
    except Exception as e:
        logger.error(f"[handle_rating] Ошибка: {e}")
        await callback.message.answer("❌ Ошибка при выставлении оценки.")