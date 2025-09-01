from typing import List, TypeVar, Generic
from pydantic.generics import GenericModel
    
    
T = TypeVar("T")

class PaginatedResponse(GenericModel, Generic[T]):
    total_items: int
    page_num: int
    page_size: int
    items: List[T]