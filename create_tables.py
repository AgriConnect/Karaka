#!/usr/bin/env python

import logging
from tortoise import run_async, Tortoise

from alarmbot.models import init_db


async def main():
    await init_db()
    # Generate the schema
    await Tortoise.generate_schemas()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('asyncpg')
    logger.setLevel(logging.DEBUG)
    run_async(main())
