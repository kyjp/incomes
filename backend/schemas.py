from typing import Optional
from pydantic import BaseModel, Field

class IncomeCreate(BaseModel):
    price: int = Field(gt=0, examples=[2500000])
    description: Optional[str] = Field(default=None, examples=['令和6年'])

class IncomeUpdate(BaseModel):
    price: Optional[str] = Field(None, gt=0, examples=[2500000])
    description: Optional[str] = Field(default=None, examples=['令和6年'])

class IncomeResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    price: int = Field(gt=0, examples=[2500000])
    description: Optional[str] = Field(None, examples=['令和6年度'])