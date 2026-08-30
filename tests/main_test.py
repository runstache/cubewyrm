"""
Tests for the Main App
"""

from assertpy import assert_that

from api.data import WarehouseTable
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


def test_return_configuration():
    """
    Tests returning the configuration
    """
