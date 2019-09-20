#!/usr/bin/env python

import logging
from tortoise import run_async, Tortoise

from alarmbot.models import init_db


async def main():
    await init_db()
    # Generate the schema
    conn = Tortoise.get_connection('default')
    await conn.execute_query('CREATE EXTENSION IF NOT EXISTS citext')
    await Tortoise.generate_schemas()
    sql = 'ALTER TABLE "user" ALTER COLUMN username TYPE CITEXT'
    await conn.execute_query(sql)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('asyncpg')
    logger.setLevel(logging.DEBUG)
    run_async(main())
