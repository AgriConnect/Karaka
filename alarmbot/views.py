from logbook import Logger
from tortoise import Tortoise
from aiohttp.web import View, view, json_response
from webargs import fields
from webargs.aiohttpparser import use_args

from .common import app, bot
from .models import User, init_db


logger = Logger(__name__)


async def init_orm(app):
    await init_db()


async def close_orm(app):
    await Tortoise.close_connections()


class SimpleView(View):
    async def get(self):
        logger.info('Request {}', self.request)
        username = self.request.match_info['username']
        user = await User.get(tg_username=username)
        logger.info('User {}', user)
        logger.info('To send message to {}', user.tg_userid)
        await bot.send_message(user.tg_userid, f'Hello {user.tg_username}')
        return json_response(f'Hello {user.tg_username}')

    @use_args({'message': fields.Str(required=True)})
    async def post(self, args):
        message = args['message']
        username = self.request.match_info['username']
        user = await User.get(tg_username=username)
        logger.info('User {}', user)
        logger.info('To send message to {}', user.tg_userid)
        await bot.send_message(user.tg_userid, message)
        return json_response(message)


app.on_startup.append(init_orm)
app.on_cleanup.append(close_orm)

app.add_routes([view('/{username}', SimpleView)])
