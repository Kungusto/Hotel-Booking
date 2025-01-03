from pydantic import BaseModel
from fastapi import Query, Depends
from typing import Annotated

class PaginationParams(BaseModel) :
    page: Annotated[int | None, Query(default=1, ge=1, lt=100),]
    per_page: Annotated[int | None, Query(default=5, ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]