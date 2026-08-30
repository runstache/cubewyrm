"""
Factories Module for creating object
"""

from api.data import WarehouseTable
from api.web import Warehouse


class WarehouseFactory:
    """
    Factory for translating Warehouse DTO Objects to the Web Interface
    """

    @staticmethod
    def to_warehouse(row: WarehouseTable) -> Warehouse:
        """
        Converts a Warehouse Table Row to the Warehouse API Response
        :return: Warehouse API response
        """
        return Warehouse(
            warehouse_id=row.warehouse_id,
            warehouse_path=row.warehouse_path,
            warehouse_description=row.warehouse_description,
        )

    @staticmethod
    def to_warehouse_table(warehouse: Warehouse) -> WarehouseTable:
        """
        Concerts a Warehouse API Object to the Warehouse Table Row
        :param warehouse: Warehouse API Object
        :return: Warehouse Table Row
        """
        return WarehouseTable(**warehouse.model_dump())
