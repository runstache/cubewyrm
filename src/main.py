"""
Main FastAPI application
"""

from fastapi import FastAPI

from api.data import WarehouseTable
from api.repositories import WarehouseRepository
from api.web import Configuration, Warehouse
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from api.factories import WarehouseFactory


url = os.getenv('DATABASE_URL', '')
engine = create_engine(url)

def create_db_and_tables() -> None:
    """
    Creates the Database Tables
    :return: None
    """
    WarehouseTable.metadata.create_all(engine)


def get_session():
    """
    Returns a SQLAlchemy Session.
    :return: Session
    """
    return Session(engine)


@asynccontextmanager
async def lifespan(app:FastAPI):
    """
    Lifespan startup for setting up the database
    :param app: FastAPI Application
    :return: None
    """
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get('/warehouses')
async def get_warehouses(page:int=1, page_size:int=100) -> list[Warehouse]:
    """
    Returns a Listing of available warehouses in the Catalog
    :param page: Page Number
    :param page_size: Page Size
    :return: List of Warehouses
    """
    with Session(engine) as session:
        repo = WarehouseRepository(session)

        if page > 1:
            result = repo.get_all(skip=page * page_size, limit=page_size)
        else:
            result = repo.get_all()

    return [WarehouseFactory.to_warehouse(x) for x in result]


@app.get('v1/config')
async def get_config(warehouse: str | None = None) -> Configuration:
    """
    All Rest Clients should call this route first. This provides the catalog configuration
    properties from the server
    :param warehouse: Warehouse name to retrieve the Catalog Configuration for.
    :return: Configuration Response
    """
    raise NotImplementedError()
