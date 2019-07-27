from pathlib import Path

from dynaconf import LazySettings


# Tell dynaconf to search in folder of this conf.py file first
config = LazySettings(ROOT_PATH_FOR_DYNACONF=Path(__file__).parent,
                      CORE_LOADERS_FOR_DYNACONF=('TOML',),
                      SETTINGS_FILE_FOR_DYNACONF=('settings.toml', '.secrets.toml'))

config.DATABASES = {
    'default': {
        'engine': 'tortoise.backends.asyncpg',
        'credentials': {
            'host': None,
            'port': 0,
            'user': None,
            'password': None,
            'database': config.DB_NAME,
        }
    },
}
