from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from schemas.request_schemas import ModuleCreate, ModuleUpdate
from schemas.response_schemas import ModuleBase
from repositories import module

from database import get_db

router = APIRouter(
    prefix = "/modules",
    tags = ["modules"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ModuleBase)
def add_module(request: ModuleCreate, db: Session = Depends(get_db)):
    return module.add_module(request, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ModuleBase)
def update_module(id: int, request: ModuleUpdate, db: Session = Depends(get_db)):
    return module.update_module(id, request, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(id: int, request: ModuleCreate, db: Session = Depends(get_db)):
    return module.delete_module(id, request, db)