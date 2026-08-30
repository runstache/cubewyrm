"""
WebAPI Contracts
"""

from pydantic import BaseModel, Field


class Warehouse(BaseModel):
    """
    Warehouse Object
    """

    warehouse_id: int | None = Field(description='Warehouse ID value', default=None)
    warehouse_path: str = Field(description='Location Path of the Warehouse')
    warehouse_description: str = Field(description='Warehouse Description')


class Configuration(BaseModel):
    """
    Configuration Data Class
    """

    overrides: dict = Field(default_factory=dict, description='Key/Value configuration overrides')
    defaults: dict = Field(default_factory=dict, description='Default configuration values')
    endpoints: list[str] = Field(default_factory=list, description='List of endpoint addresses')
    idempotency_key_lifetime: str | None = Field(
        default=None, description='Client reuse window for an Idempotency-Key (ISO-8601 duration'
    )
