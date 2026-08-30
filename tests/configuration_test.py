"""
Tests for the Configuration Endpoint
"""

from assertpy import assert_that
from sqlalchemy.orm import Session
from api.data import ConfigurationDefaultsTable, ConfigurationOverridesTable, WarehouseTable, EndpointsTable
from api.repositories import WarehouseRepository, DefaultsRepository, OverridesRepository, EndpointsRepository
from api.web import Configuration
import pytest


@pytest.fixture(scope='module', autouse=True)
def setup_tables(data_engine):
    """
    Sets up the Tables for the Tests
    """
    WarehouseTable.metadata.create_all(bind=data_engine)
    ConfigurationOverridesTable.metadata.create_all(bind=data_engine)
    ConfigurationDefaultsTable.metadata.create_all(bind=data_engine)
    EndpointsTable.metadata.create_all(bind=data_engine)



def test_return_configuration(data_engine, test_client, monkeypatch):
    """
    Tests returning the configuration
    """

    monkeypatch.setenv('IDEMPOTENT_LIFETIME', 'PT30M')

    warehouse = WarehouseTable(warehouse_path='s3://dfw/wh1', warehouse_description='Test Default Warehouse')

    with Session(data_engine) as session:
        # Add the Warehouse
        wh_repo = WarehouseRepository(session)
        wh_output = wh_repo.create(warehouse.to_dict())
        session.commit()
        session.refresh(wh_output)

        # Add the Default
        df_repo = DefaultsRepository(session)
        df_repo.create(ConfigurationDefaultsTable(warehouse_id=wh_output.warehouse_id, default_key='session_state', default_value='transient').to_dict())

        # Add the Override
        ov_repo= OverridesRepository(session)
        ov_repo.create(ConfigurationOverridesTable(warehouse_id=wh_output.warehouse_id, configuration_key='timeout', configuration_value='200ms').to_dict())

        # Add the Endpoints
        ep_repo=EndpointsRepository(session)
        ep_repo.create(EndpointsTable(endpoint='GET /v1/{prefix}/namespaces/{namespace}').to_dict())
        session.commit()

    result = test_client.get('/v1/config', params={'warehouse': 's3://dfw/wh1'})
    assert_that(result.status_code).is_equal_to(200)

    content = result.json()
    config = Configuration(**content)

    assert_that(config.defaults).contains_entry({'session_state': 'transient'})
    assert_that(config.overrides).contains_entry({'timeout': '200ms'})

    assert_that(config.endpoints).contains('GET /v1/{prefix}/namespaces/{namespace}')
    assert_that(config.idempotency_key_lifetime).is_equal_to('PT30M')

def test_get_configuration_bad_warehouse(data_engine, test_client, monkeypatch):
    """
    Tests Retrieving the configuration for a warehouse that does not exist
    """

    result = test_client.get('/v1/config', params={'warehouse': 's3://dfnone/wh1'})
    assert_that(result.status_code).is_equal_to(404)
    content = result.json()

    assert_that(content).is_equal_to({'error': {'code': 404, 'message': 'The given warehouse does not exist.', 'type': 'NoSuchWarehouseException'}})

def test_no_overrides_or_defaults(data_engine, test_client, monkeypatch):
    """
    Tests Retrieving the configuration for a warehouse without any overides or defaults
    """

    monkeypatch.setenv('IDEMPOTENT_LIFETIME', 'PT30M')

    warehouse = WarehouseTable(warehouse_path='s3://dfw/wh2', warehouse_description='Test 2 Default Warehouse')

    with Session(data_engine) as session:
        # Add the Warehouse
        wh_repo = WarehouseRepository(session)
        wh_output = wh_repo.create(warehouse.to_dict())
        session.commit()
        session.refresh(wh_output)

    result = test_client.get('/v1/config', params={'warehouse': 's3://dfw/wh2'})
    assert_that(result.status_code).is_equal_to(200)

    config = Configuration(**result.json())

    assert_that(config.defaults).is_empty()
    assert_that(config.overrides).is_empty()
    assert_that(config.idempotency_key_lifetime).is_equal_to('PT30M')









