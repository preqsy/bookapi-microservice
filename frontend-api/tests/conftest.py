from httpx import AsyncClient
import pytest

from core.db import get_db
from main import app
from tests.sample_datas.testdb import engine, mock_get_db
from models import auth_user


@pytest.fixture(
    autouse=True,
)
def create_and_drop_db():
    # Drop Table
    auth_user.Base.metadata.drop_all(bind=engine)

    # Create table
    auth_user.Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    client = AsyncClient(app=app, base_url="https://127.0.0.1/")
    yield client


@pytest.fixture(autouse=True)
def database_override_dependencies():
    app.dependency_overrides[get_db] = mock_get_db
    yield
    app.dependency_overrides = {}
