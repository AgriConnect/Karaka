
from logbook.compat import LoggingHandler
from aiohttp.web import Application
from aiogram import Bot, Dispatcher

from .conf import config


PROJECT_NAME = 'alarmbot'

app = Application()

# Initialize bot and dispatcher
bot = Bot(token=config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)

LoggingHandler().push_application()
