from pydantic import BaseModel
from typing import Union


class UserPayload(BaseModel):
    id: Union[str, int, None] = None
    username: Union[str, None] = None
    name = Union[str, None] = None
    password = Union[str, None] = None

class LoginPayload(BaseModel):
    id: Union[str, int, None] = None
    username: Union[str, None] = None
    password = Union[str, None] = None

class ExpensePayload(BaseModel):
    id: Union[str, int, None] = None
    username: Union[str, None] = None
    amount: Union[int, None] = None
    category: Union[str, None] = None
    date: Union[str, None] = None


