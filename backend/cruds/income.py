from sqlalchemy.orm import Session
from typing import Optional
from schemas import IncomeCreate, IncomeUpdate
from models import Income

def find_all(db: Session, user_id: int):
    return db.query(Income).filter(Income.user_id == user_id).all()

def find_by_id(db: Session, id: int, user_id: int):
    return db.query(Income).filter(Income.id == id).filter(Income.user_id == user_id).first()

def find_by_description(db: Session, description: str):
    return db.query(Income).filter(Income.description.like(f"%{description}%")).all()

def find_by_year(db: Session, year: int):
    return db.query(Income).filter(Income.year == year).all()

def create(db: Session, income_create: IncomeCreate, user_id: int):
    new_income = Income(
        **income_create.model_dump(),
        user_id=user_id
    )
    db.add(new_income)
    db.commit()
    return new_income

def update(db: Session, id: int, income_update: IncomeUpdate, user_id: int):
    income = find_by_id(db, id, user_id)
    if income is None:
        return None
    income.price = income.price if income_update.price is None else income_update.price
    income.year = income.year if income_update.year is None else income_update.year
    income.description = income.description if income_update.description is None else income_update.description
    db.add(income)
    db.commit()
    return income

def delete(db: Session, id: int, user_id: int):
    income = find_by_id(db, id, user_id)
    if income is None:
        return None
    db.delete(income)
    db.commit()
    return income

