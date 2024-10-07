from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "farm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "code_name" VARCHAR(40) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(100) NOT NULL UNIQUE,
    "telegram_id" INT  UNIQUE,
    "first_name" VARCHAR(200),
    "last_name" VARCHAR(200),
    "language_code" VARCHAR(16),
    "is_superuser" BOOL NOT NULL  DEFAULT True
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "membership" (
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "farm_id" INT NOT NULL REFERENCES "farm" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_membership_user_id_99ff8c" ON "membership" ("user_id", "farm_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
