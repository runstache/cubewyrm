"""
Main FastAPI application
"""

from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse

from api.data import WarehouseTable
from api.repositories import WarehouseRepository, DefaultsRepository, OverridesRepository, \
    EndpointsRepository
from api.web import Configuration, Warehouse, CatalogException, CatalogErrorTypes
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


@app.exception_handler(CatalogException)
async def catalog_exception_handler(request:Request, exc: CatalogException):
    """
    Returns the Exception in the format expected by the Iceberg Catalog REST API.
    :param request: Request
    :param exc: Exception
    :return: JSON Response
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_content()
    )


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
        existing = repo.get_warehouse_by_path(warehouse.warehouse_path)
        if existing is not None:
            output = repo.update(existing, warehouse.model_dump(exclude={'warehouse_id'}))
        else:
            output = repo.create(warehouse.model_dump())

        session.commit()
        session.refresh(output)
    return WarehouseFactory.to_warehouse(output)

@app.get('/v1/config')
async def get_config(warehouse: str) -> Configuration:
    """
    All Rest Clients should call this route first. This provides the catalog configuration
    properties from the server
    :param warehouse: Warehouse path to retrieve the Catalog Configuration for.
    :return: Configuration Response
    """

    idempotent_key = os.getenv('IDEMPOTENT_LIFETIME')

    with Session(engine) as session:
        warehouse_repo = WarehouseRepository(session)
        warehouse_item = warehouse_repo.get_warehouse_by_path(warehouse)
        if warehouse_item is None:
            raise CatalogException('The given warehouse does not exist.', CatalogErrorTypes.NO_SUCH_WAREHOUSE, 404)

        def_repo = DefaultsRepository(session)
        defaults = def_repo.get_defaults(warehouse_item.warehouse_id)

        ov_repo = OverridesRepository(session)
        overrides = ov_repo.get_overrides(warehouse_item.warehouse_id)

        ep_repo = EndpointsRepository(session)
        endpoints = ep_repo.get_all()

        defs = {x.default_key:x.default_value for x in defaults}
        ovrs = {x.configuration_key: x.configuration_value for x in overrides}
        ends = [x.endpoint for x in endpoints]

        return Configuration(overrides=ovrs, defaults=defs, idempotency_key_lifetime=idempotent_key, endpoints=ends)

