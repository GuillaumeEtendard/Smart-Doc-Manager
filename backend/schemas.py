from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
    data: str
    type: str
    date: datetime
    name: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True
