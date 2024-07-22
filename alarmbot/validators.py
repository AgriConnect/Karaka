from typing import Annotated
from pydantic.dataclasses import dataclass
from pydantic.types import StringConstraints


@dataclass
class User:
    username: Annotated[str, StringConstraints(pattern='[-_a-z0-9]+', strip_whitespace=True)]
    telegram_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    language_code: str | None = None
