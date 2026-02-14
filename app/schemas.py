from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID


class PostCreate(BaseModel):
    title: str
    content: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PostResponse(PostCreate):
    id: UUID
    owner: UserOut
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PostWithVotes(PostResponse):
    votes: int = 0
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[UUID] = None


class VoteModel(BaseModel):
    post_id: UUID
    dir: Literal[0, 1]
