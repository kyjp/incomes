from fastapi import APIRouter, Path, Query, HTTPException
from starlette import status
from cruds import income as income_cruds
from schemas import IncomeCreate, IncomeUpdate, IncomeResponse

router = APIRouter(prefix="/incomes", tags=["incomes"])

@router.get('/', response_model=list[IncomeResponse], status_code=status.HTTP_200_OK)
async def find_all():
    return income_cruds.find_all()

@router.get('/{id}', response_model=IncomeResponse, status_code=status.HTTP_200_OK)
async def find_by_id(id: int=Path(gt=0)):
    found_income = income_cruds.find_by_id(id)
    if not found_income:
        raise HTTPException(status_code=404, detail="Income not found")
    return found_income

@router.get('/', response_model=list[IncomeResponse], status_code=status.HTTP_200_OK)
async def find_by_description(description: str = Query(min_length=2, max_length=20)):
    return income_cruds.find_by_description(description)

@router.post('', response_model=IncomeResponse, status_code=status.HTTP_201_CREATED)
async def create(income_create: IncomeCreate):
    return income_cruds.create(income_create)

@router.put('/{id}', response_model=IncomeResponse, status_code=status.HTTP_200_OK)
async def update(income_update=IncomeUpdate, id: int=Path(gt=0)):
    updated_income = income_cruds.update(id, income_update)
    if not updated_income:
        raise HTTPException(status_code=404, detail="Income not updated")
    return updated_income

@router.delete('/{id}', response_model=IncomeResponse, status_code=status.HTTP_200_OK)
async def delete(id: int=Path(gt=0)):
    deleted_income = income_cruds.delete(id)
    if not deleted_income:
        raise HTTPException(status_code=404, detail="Income not deleted")
    return deleted_income
