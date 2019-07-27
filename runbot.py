#!/usr/bin/env python3

import logging
import asyncio

import logbook
from logbook import Logger
from aiogram.utils.executor import Executor
from tortoise import Tortoise

from alarmbot.loghandlers import ColorizedStderrHandler
from alarmbot.models import init_db
from alarmbot.receptionist import dp


# Configure logging
logger = Logger(__name__)
logger.handlers.append(ColorizedStderrHandler())


async def init_orm(dispatcher):
    await init_db()


async def close_orm(dispatcher):
    await Tortoise.close_connections()


if __name__ == '__main__':
    logger.level = logbook.DEBUG
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    executor = Executor(dp, skip_updates=True, loop=loop)
    logger.info('{}', executor)
    executor.on_startup(init_orm, polling=True)
    executor.on_shutdown(close_orm, polling=True)
    # executor.set_webhook(web_app=app)
    # executor.run_app(port=8000)
    executor.start_polling()
