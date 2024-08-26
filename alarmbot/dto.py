from typing import Annotated

from pydantic import BaseModel, StringConstraints
from annotated_types import Gt, MaxLen
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import User


UserDto = pydantic_model_creator(User)


class UserInput(BaseModel):
    username: Annotated[str, StringConstraints(pattern='[-_a-z0-9]+', strip_whitespace=True)]
    telegram_id: Annotated[int | None, Gt(0)]
    first_name: Annotated[str | None, MaxLen(200)]
    last_name : Annotated[str | None, MaxLen(200)]
    language_code : Annotated[str | None, MaxLen(16)]
