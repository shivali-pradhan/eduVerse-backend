from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractParams, BaseRawParams, RawParams
from pydantic import Field

from fastapi import Query
from typing import List, TypeVar, Generic
from pydantic import BaseModel
from pydantic.generics import GenericModel

# class CustomParams(AbstractParams):
#     page_size: int =  Field(20, ge=1, le=50, description="Number of items per page")
#     page_number: int =  Field(1, ge=1, description="Page number to retrieve")
#     include_total: bool = True

#     def to_raw_params(self) -> BaseRawParams:
#         return BaseRawParams(
#             limit=self.page_size,
#             offset=(self.page_number - 1) * self.page_size,
#             include_total=self.include_total,
#         )
    
class CustomParams(BaseModel, AbstractParams):
        page_number: int = Field(1, ge=1, alias="page")  # Custom alias for 'page'
        size: int = Field(20, ge=1, le=100, alias="size") # Custom alias for 'size'
        include_total: bool = True # Control if total count is included

        def to_raw_params(self) -> RawParams:
            return RawParams(
                limit=self.size,
                offset=(self.page_number - 1) * self.size,
                include_total=self.include_total,
            )

# class CustomPaginationParams(AbstractParams):
#     page_size: int = Field(2, ge=1, description="Page number to retrieve", alias="page") # Renamed 'skip' to 'page'
#     page_number: int = Field(10, ge=1, le=10, description="Number of items per page") # Renamed 'limit' to 'page_size'
#     include_total: bool = True

#     def to_raw_params(self) -> BaseRawParams:
#         return BaseRawParams(
#             limit=self.page_size,
#             offset=(self.page_number - 1) * self.page_size,
#             include_total=self.include_total,
#         )
    
T = TypeVar("T")

class PaginatedResponse(GenericModel, Generic[T]):
    total_items: int
    page_num: int
    page_size: int
    items: List[T]