from pydantic.dataclasses import dataclass
from pydantic.types import constr


@dataclass
class User:
    username: constr(regex='[-_a-z0-9]+', strip_whitespace=True) = ...
    telegram_id: int = None
    first_name: str = None
    last_name: str = None
    language_code: str = None
