from pathlib import Path

from aiohttp.web import Application
from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from .conf import config


PROJECT_NAME = 'alarmbot'
LOCALES_DIR = Path(__file__).parent.parent / 'locales'

app = Application()

# Initialize bot and dispatcher
bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher()
i18n = I18n(path=LOCALES_DIR, default_locale='en', domain=PROJECT_NAME)
i18n_middleware = SimpleI18nMiddleware(i18n)

