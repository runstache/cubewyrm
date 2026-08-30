"""
Main FastAPI application
"""

from fastapi import FastAPI, HTTPException, status

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

@app.get('/warehouses/{warehouse_id}')
async def get_warehouse(warehouse_id: int) -> Warehouse | None:
    """
    Returns the Warehouse by Primary Key
    :param warehouse_id: Warehouse ID
    :return: Warehouse
    """

    with Session(engine) as session:
        repo = WarehouseRepository(session)
        item = repo.get(warehouse_id)

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Warehouse with id: {warehouse_id} does not exist.')

    return WarehouseFactory.to_warehouse(item)


@app.post('/warehouses')
async def create_warehouse(warehouse: Warehouse) -> Warehouse:
    """
    Creates a new Warehouse in the Catalog
    :param warehouse: Warehouse.
    :return: Warehouse
    """
    with Session(engine) as session:
        repo = WarehouseRepository(session)
        existing = repo.get_warehouse_by_name(warehouse.warehouse_name)
        if existing is not None:
            output = repo.update(existing, warehouse.model_dump(exclude={'warehouse_id'}))
        else:
            output = repo.create(warehouse.model_dump())

        session.commit()
        session.refresh(output)
    return WarehouseFactory.to_warehouse(output)

@app.get('v1/config')
async def get_config(warehouse: str | None = None) -> Configuration:
    """
    All Rest Clients should call this route first. This provides the catalog configuration
    properties from the server
    :param warehouse: Warehouse name to retrieve the Catalog Configuration for.
    :return: Configuration Response
    """
    raise NotImplementedError()
