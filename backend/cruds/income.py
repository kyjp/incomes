from typing import Optional
from schemas import IncomeCreate, IncomeUpdate

class Income:
    def __init__(
        self,
        id: int,
        price: int,
        description: Optional[str]
    ):
        self.id = id
        self.price = price
        self.description = description

incomes = [
    Income(1, 3475000, '令和2年度'),
    Income(2, 3575000, '令和3年度'),
    Income(3, 3700000, '令和4年度'),
    Income(4, 3984000, '令和5年度'),
]

def find_all():
    return incomes

def find_by_id(id: int):
    for income in incomes:
        if income.id == id:
            return income
    return None

def find_by_description(description: str):
    filtered_incomes = []
    for income in incomes:
        if description in income.description:
            filtered_incomes.append(income)
    return filtered_incomes

def create(income_create: IncomeCreate):
    new_income = Income(
        len(incomes) + 1,
        income_create.price,
        income_create.description
    )
    incomes.append(new_income)
    return new_income

def update(id: int, income_update: IncomeUpdate):
    for income in incomes:
        if income.id == id:
            income.price = income.price if income_update.price is None else income_update.price
            income.description = income.description if income_update.description is None else income_update.description
    return None

def delete(id: int):
    for i in range(len(incomes)):
        if incomes[i].id == id:
            delete_income = incomes.pop(i)
            return delete_income
    return None

