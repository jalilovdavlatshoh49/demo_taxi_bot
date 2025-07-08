from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def driver_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔛 Онлайн"), KeyboardButton(text="🔴 Офлайн")],
            [KeyboardButton(text="🚖 Заказать такси"), KeyboardButton(text="🧑‍✈️ Водитель")]
        ],
        resize_keyboard=True
    )