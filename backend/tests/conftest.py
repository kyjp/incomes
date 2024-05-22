import os
import sys

app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(app_dir)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker
from models import Base, Income
from schemas import DecodedToken
from main import app
from database import get_db
from cruds.auth import get_current_user

@pytest.fixture()
def session_fixture():
    engine = create_engine(
        url="sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db=SessionLocal()
    try:
        income1 = Income(price=1000000, description="test1", user_id=1, year=2023)
        income2 = Income(price=2000000, description="test2", user_id=2, year=2024)
        db.add(income1)
        db.add(income2)
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture()
def user_fixture():
    return DecodedToken(username="user1", email="user1@example.com", user_id=1)

@pytest.fixture()
def client_fixture(session_fixture: Session, user_fixture: DecodedToken):
    def override_get_db():
        return session_fixture
    def override_get_current_user():
        return user_fixture
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()