import dataclasses
from .validators import User


class UserSerializer:
    def __init__(self, indata: dict):
        keys = User.__dataclass_fields__.keys()
        data = {k: indata[k] for k in keys if k in indata}
        self.instance = User(**data)

    @classmethod
    def _field_names(cls):
        return User.__dataclass_fields__.keys()

    def as_dict(self):
        return dataclasses.asdict(self.instance)
