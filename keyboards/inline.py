from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def rating_kb() -> InlineKeyboardMarkup:
    """Клавиатура для оценки от 1 до 5."""
    stars_row = [
        InlineKeyboardButton(text=f"{i} ⭐", callback_data=f"rate_{i}")
        for i in range(1, 6)
    ]
    return InlineKeyboardMarkup(inline_keyboard=[stars_row])


def confirm_rating_kb() -> InlineKeyboardMarkup:
    """Клавиатура для подтверждения рейтинга."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👍 Подтвердить", callback_data="confirm_rating")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_rating")]
    ])


def driver_request_kb(user_id: int) -> InlineKeyboardMarkup:
    """Клавиатура для водителя: принять или отклонить заказ."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Принять", callback_data=f"accept_{user_id}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{user_id}")
        ]
    ])


def delivered_kb() -> InlineKeyboardMarkup:
    """Кнопка подтверждения доставки/прибытия."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Доставлен", callback_data="delivered")]
    ])


def cancel_action_kb(callback_data: str = "cancel") -> InlineKeyboardMarkup:
    """Глобальная кнопка отмены действия."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data=callback_data)]
    ])
    
    


def rating_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐", callback_data="rate_1")],
        [InlineKeyboardButton(text="⭐⭐", callback_data="rate_2")],
        [InlineKeyboardButton(text="⭐⭐⭐", callback_data="rate_3")],
        [InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data="rate_4")],
        [InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data="rate_5")]
    ])