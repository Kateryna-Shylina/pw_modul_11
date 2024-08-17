from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=50)
    phone: str = Field(max_length=50)


class ContactModel(ContactBase):
    birthday_date: datetime


class ContactResponse(ContactBase):
    id: int
    birthday_date: datetime

    class Config:
        orm_mode = True