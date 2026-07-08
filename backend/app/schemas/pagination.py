from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class PaginateResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    size: int