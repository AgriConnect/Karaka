from http import HTTPStatus

from logbook import Logger
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist
from aiohttp import web
from aiohttp.web import View, view, HTTPNotFound, Response, Request
from webargs import fields
from webargs.aiohttpparser import use_args
from pydantic import BaseModel, ValidationError
from aiohttp_basicauth_middleware import basic_auth_middleware

from .conf import config
from .common import app, bot
from .models import User, init_db
from .dto import UserDto, UserInput

logger = Logger(__name__)


async def init_orm(app):
    await init_db()


async def close_orm(app):
    await Tortoise.close_connections()


# Define a function with full type annotation, accepting Pydantic model and returning a JSON response
def my_json_response(data: BaseModel, status=HTTPStatus.OK):
    return Response(text=data.model_dump_json(), status=status, content_type='application/json')



class UserView(View):
    async def get(self):
        username = self.request.match_info['username']
        try:
            user = await User.get(username=username)
        except DoesNotExist:
            return web.HTTPNotFound()
        logger.info('User {}', user)
        user_dto = await UserDto.from_tortoise_orm(user)
        return my_json_response(user_dto)


async def create_user(request: Request):
    raw_data = await request.json()
    logger.debug('Post data: {}', raw_data)
    try:
        indata = UserInput(**raw_data)
    except ValidationError as e:
        logger.error('Error: {}', e)
        return web.HTTPBadRequest()
    try:
        user = await User.get(username=indata.username)
        return web.HTTPFound(f'/users/{indata.username}')
    except DoesNotExist:
        user = await User.create(**indata.model_dump())
        user_dto = await UserDto.from_tortoise_orm(user)
        return my_json_response(user_dto, HTTPStatus.CREATED)


@use_args({'message': fields.Str(required=True), 'parse_mode': fields.Str()})
async def post_user_message(request, args):
    message = args['message']
    username = request.match_info['username']
    try:
        user = await User.get(username=username)
    except DoesNotExist:
        logger.info('User {} not found', username)
        raise HTTPNotFound(reason='User not found')
    logger.info('User {}', user)
    logger.info('To send message to {}', user.telegram_id)
    parse_mode = args.get('parse_mode')
    await bot.send_message(user.telegram_id, message, parse_mode)
    return my_json_response(message)


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
