"""
Tests for the Main App
"""

from assertpy import assert_that

from api.data import WarehouseTable
from api.factories import WarehouseFactory
from api.repositories import WarehouseRepository
from api.web import Warehouse
from sqlalchemy.orm import Session



def test_get_warehouses(data_engine, test_client):
    """
    Tests Retrieving the Warehouses from the API
    """

    warehouse = Warehouse(warehouse_id=None, warehouse_code='TST', warehouse_name='Test Warehouse')
    WarehouseTable.metadata.create_all(bind=data_engine)

    with Session(data_engine) as session:
        repo = WarehouseRepository(session)
        repo.create(warehouse.model_dump())
        session.commit()

    result = test_client.get('/warehouses')
    assert_that(result.status_code).is_equal_to(200)

    content = result.json()
    assert_that(content).contains({
        'warehouse_id': 1,
        'warehouse_code': 'TST',
        'warehouse_name': 'Test Warehouse'
    })

def test_create_warehouse(data_engine, test_client):
    """
    Tests Creating a new Warehouse
    """

    warehouse = Warehouse(warehouse_id=None, warehouse_code='TST1', warehouse_name='Test Warehouse 1')
    WarehouseTable.metadata.create_all(bind=data_engine)
    result = test_client.post('/warehouses', json=warehouse.model_dump())

    assert_that(result.status_code).is_equal_to(200)
    content = result.json()
    item = Warehouse(**content)

    with Session(data_engine) as session:
        repo = WarehouseRepository(session)
        output = repo.get(item.warehouse_id)
        assert_that(output).is_not_none()


def test_update_warehouse(data_engine, test_client):
    """
    Tests Updating an existing Warehouse
    """

    warehouse = Warehouse(warehouse_id=None, warehouse_code='TST2', warehouse_name='Test Warehouse 2')
    WarehouseTable.metadata.create_all(bind=data_engine)
    with Session(data_engine) as session:
        repo = WarehouseRepository(session)
        item = repo.create(warehouse.model_dump())
        session.commit()
        session.refresh(item)


    result = test_client.post('/warehouses', json=warehouse.model_dump())

    assert_that(result.status_code).is_equal_to(200)
    content = result.json()
    assert_that(content.get('warehouse_id', 0)).is_equal_to(item.warehouse_id)


def test_get_warehouse(data_engine, test_client):
    """
    Tests Retrieving a Warehouse from the API
    """

    warehouse = Warehouse(warehouse_id=None, warehouse_code='TST4', warehouse_name='Test Warehouse 4')
    WarehouseTable.metadata.create_all(bind=data_engine)
    with Session(data_engine) as session:
        repo = WarehouseRepository(session)
        item = repo.create(warehouse.model_dump())
        session.commit()
        session.refresh(item)

    result = test_client.get(f'/warehouses/{item.warehouse_id}')
    assert_that(result.status_code).is_equal_to(200)
    assert_that(result.json()).is_not_none()

def test_get_warehouse_not_exist(data_engine, test_client):
    """
    Tests 404 Error for Warehouse that does not exists
    """

    WarehouseTable.metadata.create_all(bind=data_engine)

    result = test_client.get('/warehouses/999')
    assert_that(result.status_code).is_equal_to(404)



def test_return_configuration():
    """
    Tests returning the configuration
    """
