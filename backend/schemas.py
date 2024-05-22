from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class IncomeCreate(BaseModel):
    price: int = Field(gt=0, examples=[2500000])
    year: int = Field(gt=0, examples=[2024])
    description: Optional[str] = Field(default=None, examples=['令和6年'])

class IncomeUpdate(BaseModel):
    price: Optional[int] = Field(None, gt=0, examples=[2500000])
    year: Optional[int] = Field(None, gt=0, examples=[2024])
    description: Optional[str] = Field(default=None, examples=['令和6年'])

class IncomeResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    price: int = Field(gt=0, examples=[2500000])
    year: int = Field(gt=0, examples=[2024])
    description: Optional[str] = Field(None, examples=['令和6年度'])
    created_at: datetime
    updated_at: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str = Field(min_length=2, examples=["user1"])
    email: str = Field(min_length=2, examples=["user1@example.com"])
    password: str = Field(min_length=8, examples=["test1234"])

class UserResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    username: str = Field(min_length=2, examples=["user1"])
    email: str = Field(min_length=2, examples=["user1@example.com"])
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenUser(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class Msg(BaseModel):
    message: str

class DecodedToken(BaseModel):
    username: str
    email: str
    user_id: int