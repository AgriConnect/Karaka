from http import HTTPStatus

from logbook import Logger
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist
from aiohttp.web import (
    Response,
    Request,
    HTTPFound,
    HTTPNotFound,
    HTTPUnprocessableEntity,
)
from pydantic import BaseModel, ValidationError
from aiohttp_basicauth_middleware import basic_auth_middleware
from aiohttp_pydantic import PydanticView  # type: ignore

from .conf import config
from .common import app, bot
from .models import User, init_db
from .dto import UserDto, UserInput, MessagePostInput

logger = Logger(__name__)


async def init_orm(app):
    await init_db()


async def close_orm(app):
    await Tortoise.close_connections()


# Define a function with full type annotation, accepting Pydantic model and returning a JSON response
def json_response(data: BaseModel, status=HTTPStatus.OK) -> Response:
    return Response(
        text=data.model_dump_json(), status=status, content_type='application/json'
    )


class UserView(PydanticView):
    async def get(self, username: str) -> Response:
        try:
            user = await User.get(username=username)
        except DoesNotExist:
            return HTTPNotFound()
        logger.info('User {}', user)
        user_dto = await UserDto.from_tortoise_orm(user)
        return json_response(user_dto)

    async def post(self, indata: UserInput) -> Response:
        try:
            user = await User.get(username=indata.username)
            return HTTPFound(f'/users/{indata.username}')
        except DoesNotExist:
            user = await User.create(**indata.model_dump())
            user_dto = await UserDto.from_tortoise_orm(user)
            return json_response(user_dto, HTTPStatus.CREATED)


async def post_user_message(request: Request) -> Response:
    try:
        indata = MessagePostInput.model_validate_json(await request.text())
    except ValidationError as e:
        raise HTTPUnprocessableEntity(body={'errors': e.errors()})
    message = indata.message
    username = request.match_info['username']
    try:
        user = await User.get(username=username)
    except DoesNotExist:
        logger.info('User {} not found', username)
        raise HTTPNotFound(reason='User not found')
    logger.info('User {}', user)
    logger.info('To send message to {}', user.telegram_id)
    await bot.send_message(user.telegram_id, message, parse_mode=indata.parse_mode)
    return json_response(indata)


app.on_startup.append(init_orm)
app.on_cleanup.append(close_orm)

app.middlewares.append(basic_auth_middleware(('/users',), dict(config.API_USERS)))

app.router.add_view('/users/{username}', UserView)
app.router.add_post('/users/{username}/message', post_user_message)
