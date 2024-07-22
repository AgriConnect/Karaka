
from tortoise.models import Model
from tortoise import Tortoise, fields
from .conf import config


class Farm(Model):
    id = fields.IntField(pk=True)
    code_name = fields.CharField(max_length=40, unique=True)


class User(Model):
    id = fields.IntField(pk=True)
    # Store fields as in https://core.telegram.org/bots/api#user
    # Even though username is optional in Telegram, we require this data,
    # to able to locate user from outside (we cannot find Telegram user by ID or phone number)
    username = fields.CharField(max_length=100, unique=True)
    telegram_id = fields.IntField(unique=True, null=True)
    first_name = fields.CharField(max_length=200, null=True)
    last_name = fields.CharField(max_length=200, null=True)
    language_code = fields.CharField(max_length=16, null=True)
    # Private info for our system
    is_superuser = fields.BooleanField(default=True)
    farms = fields.ManyToManyField('models.Farm', related_name='users', through='membership')

    def __str__(self):
        return self.username or str(self.id)


async def init_db():
    ttconfig = {
        'connections': config.DATABASES,
        'apps': {
            'models': {
                'models': ['alarmbot.models']
            }
        }
    }
    await Tortoise.init(ttconfig)
