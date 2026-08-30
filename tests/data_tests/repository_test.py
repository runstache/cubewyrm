"""
Tests the Repositories
"""

from api.repositories import WarehouseRepository
from api.web import Warehouse
from sqlalchemy.orm import Session
from assertpy import assert_that
from api.data import WarehouseTable

def test_add_item(data_engine) -> None:
    """
    Tests Adding a New warehouse to the repository
    """
    warehouse = Warehouse(warehouse_id=None, warehouse_code='TST', warehouse_name='Test Warehouse')
    WarehouseTable.metadata.create_all(bind=data_engine)

    with Session(data_engine) as session:
        repo = WarehouseRepository(session)
        result = repo.create(warehouse.model_dump())
        session.commit()
        session.refresh(result)

    assert_that(result.warehouse_id).is_not_none()


def test_update_item(data_engine):
    """
    Tests Updating a Warehouse in the Database
    """

    warehouse = Warehouse(warehouse_id=None, warehouse_code='TST-1', warehouse_name='Test Warehouse 1')
    WarehouseTable.metadata.create_all(bind=data_engine)

    with Session(data_engine) as session:
        repo = WarehouseRepository(session)
        result = repo.create(warehouse.model_dump())
        session.commit()
        session.refresh(result)

        repo.update(result, {'warehouse_code': 'TST-2'})
        session.commit()
        session.refresh(result)

    assert_that(result.warehouse_code).is_equal_to('TST-2')

def test_delete_item(data_engine):
    """
    Tests Deleting an Item from the Database
    """

    warehouse = Warehouse(warehouse_id=None, warehouse_code='TST-3', warehouse_name='Test Warehouse 3')
    WarehouseTable.metadata.create_all(bind=data_engine)

    with Session(data_engine) as session:
        repo = WarehouseRepository(session)
        result = repo.create(warehouse.model_dump())
        session.commit()
        session.refresh(result)

        pk = result.warehouse_id
        repo.delete(result)
        session.commit()

        item = repo.get(pk)
        assert_that(item).is_none()

def test_get_item(data_engine):
    """
    Tests Retrieving an item from the database
    """

    warehouse = Warehouse(warehouse_id=None, warehouse_code='TST-4', warehouse_name='Test Warehouse 4')
    WarehouseTable.metadata.create_all(bind=data_engine)

    with Session(data_engine) as session:
        repo = WarehouseRepository(session)
        result = repo.create(warehouse.model_dump())
        session.commit()
        session.refresh(result)

        pk = result.warehouse_id

        item = repo.get(pk)
        assert_that(item).is_not_none()

def test_get_page_of_items(data_engine):
    """
    Tests Retrieving all an item from the database
    """
    warehouse = Warehouse(warehouse_id=None, warehouse_code='TST-5', warehouse_name='Test Warehouse 5')
    WarehouseTable.metadata.create_all(bind=data_engine)

    with Session(data_engine) as session:
        repo = WarehouseRepository(session)
        result = repo.create(warehouse.model_dump())
        session.commit()
        session.refresh(result)

        result = repo.get_all()
        assert_that(len(result)).is_greater_than_or_equal_to(1)
