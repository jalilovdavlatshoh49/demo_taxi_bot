import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from config import API_TOKEN
from handlers import user, driver, callbacks


# Логгиринг бо формат
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    # ✅ Инициализатсияи бот ва диспетчер
    bot = Bot(token=API_TOKEN)
    bot.default_parse_mode = ParseMode.HTML
    dp = Dispatcher(storage=MemoryStorage())

    # ✅ Подключение всех роутеров
    dp.include_routers(
        user.router,
        driver.router,
        callbacks.router
    )

    logger.info("🚀 Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("🛑 Бот остановлен вручную.")