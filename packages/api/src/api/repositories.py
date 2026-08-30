"""
SQL Alchemy Repositories for interacting with the
"""

from collections.abc import Sequence
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Session

from api.data import (
    ConfigurationDefaultsTable,
    ConfigurationOverridesTable,
    EndpointsTable,
    WarehouseTable,
)

ModelType = TypeVar('ModelType', bound=DeclarativeBase)


class BaseRepository[ModelType]:
    """
    Base CRUD Repository
    """

    model: type[ModelType]
    db: Session

    def __init__(self, model: type[ModelType], db: Session):
        """
        Constructor
        :param model: Model Instance
        :param db: SB Session
        """
        self.model = model
        self.db = db

    def get(self, id_value: int) -> ModelType | None:
        """
        Retrieves a model by the ID.
        :param id_value: Identity Value
        :return: Model Instance
        """

        return self.db.get(self.model, id_value)

    def get_all(self, skip: int = 0, limit=100) -> Sequence[ModelType]:
        """
        Retrieves Pages of a given model
        :return: Sequence of Models
        """

        stmt = select(self.model).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()

    def create(self, obj_in: dict) -> ModelType:
        """
        Creates a new Instance Model in the Database
        :param obj_in: Dictionary of the Model.
        :return: Model Instance
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: dict) -> ModelType:
        """
        Updates an existing record in the database
        :param db_obj: DB Object
        :param obj_in:
        :return:
        """
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        self.db.add(db_obj)
        return db_obj

    def delete(self, db_obj: ModelType) -> None:
        """
        Deletes an existing record from the Database.
        :param db_obj: Database Object
        :return: None
        """
        self.db.delete(db_obj)


class WarehouseRepository(BaseRepository[WarehouseTable]):
    """
    Warehouse Repository for Interacting with the Warehouse table
    """

    def __init__(self, session: Session) -> None:
        """
        Constructor
        :param session: DB Session
        """
        super().__init__(WarehouseTable, session)

    def get_warehouse_by_path(self, warehouse_path:str) -> WarehouseTable | None:
        """
        Retrieved the Warehouse by its path
        :param warehouse_path: Warehouse Path
        :return: Boolean
        """

        stmt = select(self.model).where(WarehouseTable.warehouse_path == warehouse_path)
        result = self.db.scalars(stmt).all()
        return result[0] if result else None


class OverridesRepository(BaseRepository[ConfigurationOverridesTable]):
    """
    Repository for working with Configuration Overrides
    """

    def __init__(self, session: Session) -> None:
        """
        Constructor
        :param session: DB Session
        """
        super().__init__(ConfigurationOverridesTable, session)

    def get_overrides(self, warehouse_id:int) -> Sequence[ConfigurationOverridesTable]:
        """
        Retrieves the ConfigurationOverrides for a given warehouse.
        :param warehouse_id: Warehouse ID
        :return: List of ConfigurationOverrides
        """
        stmt = select(ConfigurationOverridesTable).where(ConfigurationOverridesTable.warehouse_id == warehouse_id)
        result = self.db.scalars(stmt).all()
        return result


class DefaultsRepository(BaseRepository[ConfigurationDefaultsTable]):
    """
    Repository for working with Configuration Defaults
    """

    def __init__(self, session: Session) -> None:
        """
        Constructor
        :param session: DB Session
        """
        super().__init__(ConfigurationDefaultsTable, session)


    def get_defaults(self, warehouse_id:int) -> Sequence[ConfigurationDefaultsTable]:
        """
        Retrieves the Configuration Defaults for a given warehouse.
        :param warehouse_id: Warehouse ID
        :return: Sequence of ConfigurationDefaults
        """
        stmt = select(ConfigurationDefaultsTable).where(ConfigurationDefaultsTable.warehouse_id == warehouse_id)
        result = self.db.scalars(stmt).all()
        return result

class EndpointsRepository(BaseRepository[EndpointsTable]):
    """
    Repository for working with Endpoints
    """

    def __init__(self, session: Session) -> None:
        """
        Constructor
        :param session: DB Session
        """
        super().__init__(EndpointsTable, session)
