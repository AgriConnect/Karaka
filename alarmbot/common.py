from pathlib import Path

from logbook.compat import LoggingHandler
from aiohttp.web import Application
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from .conf import config


PROJECT_NAME = 'alarmbot'
LOCALES_DIR = Path(__file__).parent.parent / 'locales'

app = Application()

# Initialize bot and dispatcher
bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)
i18n = I18nMiddleware(PROJECT_NAME, LOCALES_DIR)
dp.middleware.setup(i18n)

LoggingHandler().push_application()
