
from tortoise.models import Model
from tortoise import Tortoise, fields
from .conf import config


class Farm(Model):
    id = fields.IntField(pk=True)
    code_name = fields.CharField(max_length=40, unique=True)


class User(Model):
    id = fields.IntField(pk=True)
    tg_username = fields.CharField(max_length=100, unique=True, null=True)
    tg_userid = fields.IntField(unique=True, null=True)
    is_superuser = fields.BooleanField(default=True)
    farms = fields.ManyToManyField('models.Farm', related_name='users', through='membership')


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
