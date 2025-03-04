from pydantic import BaseModel
from typing import Union


class UserPayload(BaseModel):
    username: Union[str, None] = None
    name: Union[str, None] = None
    password: Union[str, None] = None

class LoginPayload(BaseModel):
    username: Union[str, None] = None
    password: Union[str, None] = None

class ExpensePayload(BaseModel):
    username: Union[str, None] = None
    amount: Union[int, None] = None
    category: Union[str, None] = None
    date: Union[str, None] = None


