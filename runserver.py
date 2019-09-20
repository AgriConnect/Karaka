#!/usr/bin/env python3

import logging
import asyncio

import click
import logbook
from logbook import Logger
from aiogram.utils.executor import Executor

from alarmbot.loghandlers import ColorizedStderrHandler


# Configure logging
logger = Logger(__name__)
logger.handlers.append(ColorizedStderrHandler())


@click.command()
@click.option('-s', '--socket-path', type=click.Path())
@click.argument('port', default=8006, type=int)
def main(socket_path, port):
    from alarmbot.views import app
    from alarmbot.receptionist import dp
    logger.level = logbook.DEBUG
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    executor = Executor(dp, skip_updates=True, loop=loop)
    logger.info('{}', executor)
    executor.set_webhook(web_app=app)
    if not socket_path:
        executor.run_app(port=port)
    else:
        executor.run_app(path=socket_path)


if __name__ == '__main__':
    main()
