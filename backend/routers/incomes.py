from typing import Annotated
from fastapi import APIRouter, Path, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from cruds import income as income_cruds, auth as auth_cruds
from schemas import IncomeCreate, IncomeUpdate, IncomeResponse, DecodedToken
from database import get_db

DbDependency = Annotated[Session, Depends(get_db)]
UserDependency = Annotated[DecodedToken, Depends(auth_cruds.get_current_user)]
router = APIRouter(prefix="/incomes", tags=["incomes"])

@router.get('', response_model=list[IncomeResponse], status_code=status.HTTP_200_OK)
async def find_all(db: DbDependency, user: UserDependency):
    return income_cruds.find_all(db, user.user_id)

@router.get('/{id}', response_model=IncomeResponse, status_code=status.HTTP_200_OK)
async def find_by_id(db:DbDependency, user: UserDependency, id: int=Path(gt=0)):
    found_income = income_cruds.find_by_id(db, id, user.user_id)
    if not found_income:
        raise HTTPException(status_code=404, detail="Income not found")
    return found_income

@router.get('/', response_model=list[IncomeResponse], status_code=status.HTTP_200_OK)
async def find_by_description(db: DbDependency, description: str = Query(min_length=2, max_length=20)):
    return income_cruds.find_by_description(db, description)

@router.get('/year/{year}', response_model=list[IncomeResponse], status_code=status.HTTP_200_OK)
async def find_by_year(db: DbDependency, year: int=Path(gt=0)):
    return income_cruds.find_by_year(db, year)

@router.post('', response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
async def create(db: DbDependency, user: UserDependency, income_create: IncomeCreate):
    return income_cruds.create(db, income_create, user.user_id)

@router.put('/{id}', response_model=IncomeResponse, status_code=status.HTTP_200_OK)
async def update(db: DbDependency, user: UserDependency, income_update: IncomeUpdate, id: int=Path(gt=0)):
    updated_income = income_cruds.update(db, id, income_update, user.user_id)
    if not updated_income:
        raise HTTPException(status_code=404, detail="Income not updated")
    return updated_income

@router.delete('/{id}', response_model=IncomeResponse, status_code=status.HTTP_200_OK)
async def delete(db:DbDependency, user:UserDependency, id: int=Path(gt=0)):
    deleted_income = income_cruds.delete(db, id, user.user_id)
    if not deleted_income:
        raise HTTPException(status_code=404, detail="Income not deleted")
    return deleted_income
