from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint




class User(BaseModel):
    id: int
    email: EmailStr
    # created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostAuthor(BaseModel):
    id: int
    email: EmailStr


class Post(PostBase):
    id: int
    created_at: datetime
    # owner_id: int
    author: PostAuthor

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]


class Vote(BaseModel):
    post_id: int
    dir: int


class PostVotes(BaseModel):
    Post: Post
    votes: int
