from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from schemas.request_schemas import ModuleCreate, ModuleUpdate
from schemas.response_schemas import ModuleBase, ModuleResponse
from schemas.token_schemas import CurrentUser
from auth.dependencies import require_instructor, get_current_user
from services import module

from database import get_db

router = APIRouter(
    prefix = "/modules",
    tags = ["modules"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ModuleBase)
def add_module(request: ModuleCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return module.add_module(request, db, current_user)

@router.get("/{id}", response_model=ModuleResponse)
def get_module(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return module.get_module(id, db, current_user)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ModuleBase)
def update_module(id: int, request: ModuleUpdate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return module.update_module(id, request, db, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return module.delete_module(id, db, current_user)


@router.post("/{id}/uploadfile", status_code=status.HTTP_201_CREATED)
async def upload_file(id: int, file: UploadFile, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return module.save_file(id, db, current_user, file)