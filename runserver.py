#!/usr/bin/env python3

import logging
import asyncio

import logbook
from logbook import Logger
from aiogram.utils.executor import Executor

from alarmbot.loghandlers import ColorizedStderrHandler
from alarmbot.views import app
from alarmbot.receptionist import dp


# Configure logging
logger = Logger(__name__)
logger.handlers.append(ColorizedStderrHandler())


if __name__ == '__main__':
    logger.level = logbook.DEBUG
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    executor = Executor(dp, skip_updates=True, loop=loop)
    logger.info('{}', executor)
    executor.set_webhook(web_app=app)
    executor.run_app(port=8000)
