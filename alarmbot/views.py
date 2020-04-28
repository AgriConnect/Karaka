from logbook import Logger
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist
from aiohttp import web
from aiohttp.web import View, view, json_response
from webargs import fields
from webargs.aiohttpparser import use_args
from pydantic.error_wrappers import ValidationError
from aiohttp_basicauth_middleware import basic_auth_middleware

from .conf import config
from .common import app, bot
from .models import User, init_db
from .serializers import UserSerializer

logger = Logger(__name__)


async def init_orm(app):
    await init_db()


async def close_orm(app):
    await Tortoise.close_connections()


class UserView(View):
    async def get(self):
        username = self.request.match_info['username']
        try:
            user = await User.get(username=username)
        except DoesNotExist:
            return web.HTTPNotFound()
        logger.info('User {}', user)
        logger.info('To send message to {}', user.telegram_id)
        keys = UserSerializer._field_names()
        return json_response({k: getattr(user, k) for k in keys})


async def create_user(request):
    indata = await request.json()
    logger.debug('Post data" {}', indata)
    try:
        serializer = UserSerializer(indata)
    except ValidationError as e:
        logger.error('{}', e)
        return web.HTTPBadRequest()
    cdata = serializer.as_dict()
    username = cdata['username']
    try:
        user = await User.get(username=username)
        return web.HTTPFound(f'/users/{username}')
    except DoesNotExist:
        user = await User.create(**cdata)
    keys = serializer._field_names()
    return json_response({k: getattr(user, k) for k in keys},
                         status=201)


@use_args({'message': fields.Str(required=True), 'parse_mode': fields.Str()})
async def post_user_message(request, args):
    message = args['message']
    username = request.match_info['username']
    user = await User.get(username=username)
    logger.info('User {}', user)
    logger.info('To send message to {}', user.telegram_id)
    parse_mode = args['parse_mode']
    await bot.send_message(user.telegram_id, message, parse_mode)
    return json_response(message)


app.on_startup.append(init_orm)
app.on_cleanup.append(close_orm)

app.middlewares.append(
    basic_auth_middleware(
        ('/users',),
        dict(config.API_USERS)
    )
)

app.add_routes([view('/users/{username}', UserView),
                web.post('/users/', create_user),
                web.post('/users/{username}/message', post_user_message)])
