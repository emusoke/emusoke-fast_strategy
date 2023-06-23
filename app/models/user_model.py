from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    username: Union[str, None] = None
    password: str
