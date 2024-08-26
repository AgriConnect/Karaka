#!/usr/bin/env python3

import os
import logging
import logging.config
import socket
import importlib.util

import click
import logbook
from logbook import Logger
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from chameleon_log.detectors import is_connected_journald
from chameleon_log.amend import StdLoggingHandler

from alarmbot.consts import WEBHOOK_PATH
from alarmbot.conf import config
from alarmbot.loghandlers import ColorizedStderrHandler


# Configure logging
INSIDE_SYSTEMD = bool(importlib.util.find_spec('systemd')) and is_connected_journald()
PROD_LOGGING = {
    'formatters': {
        'tiny': {
            'format': '%(message)s',
            'datefmt': '[%X]',
        }
    },
    'handlers': {
        'journald': {
            'class': 'systemd.journal.JournalHandler',
            'formatter': 'tiny',
        }
    },
    'root': {'handlers': ['journald'], 'level': 'INFO'},
}
logger = Logger(__name__)


@click.command()
@click.option('-s', '--socket-path', type=click.Path())
@click.argument('port', default=8006, type=int)
def main(socket_path, port):
    from alarmbot.common import bot, dp
    from alarmbot.views import app
    from alarmbot.receptionist import on_startup, router

    logger.level = logbook.DEBUG
    if INSIDE_SYSTEMD:
        logging.config.dictConfig(PROD_LOGGING)
        StdLoggingHandler().push_application()
    else:
        logging.basicConfig(level=logging.INFO)
        ColorizedStderrHandler().push_application()
    dp.include_router(router)
    dp.startup.register(on_startup)
    webhook_request_handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=config.WEBHOOK_SECRET
    )
    # Register webhook handler on application
    webhook_request_handler.register(app, path=WEBHOOK_PATH)
    logger.info('Registered webwook handlers at {} for bot.', WEBHOOK_PATH)
    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)
    logger.debug('Routes: {}', app.router.routes()._routes)
    token_head = bot.token.split(':')[0]
    if socket_path:
        # Make socket file writable by Nginx
        sk = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            os.remove(socket_path)
        except FileNotFoundError:
            pass
        sk.bind(socket_path)
        os.chmod(socket_path, 0o664)
        logger.info(
            'To run web application for bot {}, listening at {}',
            token_head,
            socket_path,
        )
        web.run_app(app, sock=sk)
    else:
        logger.info(
            'To run web application for bot {}, listening on port {}', token_head, port
        )
        web.run_app(app, port=port)


if __name__ == '__main__':
    main()
