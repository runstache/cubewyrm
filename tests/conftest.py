"""
Pytest Fixtures
"""
import os

import pytest
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer

from fastapi.testclient import TestClient


@pytest.fixture(scope='session')
def postgres_container():
    """
    Postgres Container Fixture
    """
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        yield postgres



@pytest.fixture(scope='module')
def data_engine(postgres_container):
    """
    Creates a SQLLite Database
    """
    url = postgres_container.get_connection_url()
    os.environ['DATABASE_URL'] = url
    engine = create_engine(url)
    return engine

@pytest.fixture(scope='module')
def test_client():
    """
    Creates a Test Client for the application
    """
    from main import app

    client = TestClient(app)
    return client

