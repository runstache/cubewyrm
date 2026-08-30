"""
WebAPI Contracts
"""

from pydantic import BaseModel, Field
from enum import StrEnum

class CatalogErrorTypes(StrEnum):
    """
    Catalog Error Types
    """
    NO_SUCH_WAREHOUSE = 'NoSuchWarehouseException'
    BAD_REQUEST = 'BadRequestException'
    NOT_AUTHORIZED = 'NotAuthorizedException'
    AUTH_TIMEOUT = 'AuthenticationTimeoutException'
    SLOW_DOWN = 'SlowDownException'
    SERVER_ERROR = 'InternalServerError'



class CatalogException(Exception):
    """
    Specific Catalog Exception Handler Class
    """

    message: str
    error_type:str
    status_code:int

    def __init__(self, message:str, error_type:str, status_code:int):
        """
        Constructor.
        :param message: Error Message
        :param error_type:  Error Type
        :param status_code: Status Code
        """
        self.message = message
        self.error_type = error_type
        self.status_code = status_code

    def to_content(self) -> dict:
        """
        Returns the Content for the Error in the expected Iceberg Catalog API format
        :return: Dictionary
        """

        return {
            'error': {
                'message': self.message,
                'type': self.error_type,
                'code': self.status_code
            }
        }


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
