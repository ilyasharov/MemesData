from pydantic import BaseModel, Field
from typing import List

class MemeBase(BaseModel):
    title: str
    description: str
    url: str

class MemeCreate(MemeBase):
    image: bytes

class MemeUpdate(BaseModel):
    title: str = None
    description: str = None
    image: bytes = None

class Meme(MemeBase):
    id: int
    image_url: str

    class Config:
        orm_mode = True

class MemeList(BaseModel):
    items: List[Meme]
    total: int
    page: int
    size: int
