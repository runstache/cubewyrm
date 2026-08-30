"""
Data Access Objects
"""

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WarehouseTable(Base):
    """
    Configured Warehouses
    """

    __tablename__ = 'warehouses'

    warehouse_id: Mapped[int] = mapped_column(
        'warehouse_id', BigInteger, primary_key=True, autoincrement=True, index=True
    )
    warehouse_code: Mapped[str] = mapped_column('warehouse_code', String(50))
    warehouse_name: Mapped[str] = mapped_column('warehouse_name', String(150))

    def __repr__(self):
        return (
            f'WarehouseTable(warehouse_id={self.warehouse_id}, '
            f'warehouse_code={self.warehouse_code}, '
            f'warehouse_name={self.warehouse_name})'
        )


class ConfigurationOverridesTable(Base):
    """
    Server Configuration Table
    """

    __tablename__ = 'overrides'

    override_id: Mapped[int] = mapped_column(
        'override_id', BigInteger, primary_key=True, autoincrement=True
    )
    warehouse_id: Mapped[int] = mapped_column('warehouse_id', BigInteger)
    configuration_key: Mapped[str] = mapped_column('configuration_key', String(50))
    configuration_value: Mapped[str] = mapped_column('configuration_value', String(255))

    def __repr__(self):
        return (
            f'ConfigurationOverrideTable(override_id={self.override_id}, '
            f'warehouse_id={self.warehouse_id}, configuration_key={self.configuration_key}, '
            f'configuration_value={self.configuration_value})'
        )


class ConfigurationDefaultsTable(Base):
    """
    Server Configuration Defaults
    """

    __tablename__ = 'defaults'

    default_id: Mapped[int] = mapped_column(
        'default_id', BigInteger, primary_key=True, autoincrement=True
    )
    warehouse_id: Mapped[int] = mapped_column('warehouse_id', BigInteger)
    default_key: Mapped[str] = mapped_column('default_key', String(50))
    default_value: Mapped[str] = mapped_column('default_value', String(255))

    def __repr__(self):
        return (
            f'ConfigurationDefaultsTable(default_id={self.default_id}, '
            f'warehouse_id={self.warehouse_id}, default_key={self.default_key}, '
            f'default_value={self.default_value})'
        )


class EndpointsTable(Base):
    """
    Server Endpoints Table
    """

    __tablename__ = 'endpoints'

    endpoint_id: Mapped[int] = mapped_column(
        'endpoint_id', BigInteger, primary_key=True, autoincrement=True
    )
    endpoint: Mapped[str] = mapped_column('endpoint', String(255))

    def __repr__(self):
        return f'EndpointTable(endpoint_id={self.endpoint_id}, endpoint={self.endpoint})'
