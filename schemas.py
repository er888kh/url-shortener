import datetime

from pydantic import BaseModel
from pydantic import constr


class ShortenerBase(BaseModel):
    url: str
    expire_time: datetime.datetime


class ShortenerCreate(ShortenerBase):
    pass


class Shortener(ShortenerBase):
    id: int
    shortened: str
    token: str
    visits: int

    class Config:
        orm_mode = True


class ShortenerNoSecret(ShortenerBase):
    id: int
    shortened: str
    visits: int

    class Config:
        orm_mode = True


class ShortenerDelete(BaseModel):
    shortened: constr(to_lower=True, max_length=20, regex=r"^[a-z0-9]+$")
    token: constr(to_lower=True, max_length=30, regex=r"^[a-z0-9]+$")


class ShortenerUpdate(ShortenerBase):
    shortened: str  # The previous url
    token: str  # The secret