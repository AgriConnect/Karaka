from pathlib import Path

from dynaconf import Dynaconf


# Tell dynaconf to search in folder of this conf.py file first
config = Dynaconf(
    root_path=Path(__file__).parent,
    core_loaders=("TOML",),
    environments=True,
    settings_files=("settings.toml", ".secrets.toml"),
)

config.DATABASES = {
    "default": {
        "engine": "tortoise.backends.asyncpg",
        "credentials": {
            "host": None,
            "port": 0,
            "user": None,
            "password": None,
            "database": config.DB_NAME,
        },
    },
}
