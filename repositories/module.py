from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models.course_models import Module
from schemas.request_schemas import ModuleCreate, ModuleUpdate
from schemas.token_schemas import CurrentUser
from .course import check_instructor_course

def add_module(request: ModuleCreate, db: Session, current_instructor: CurrentUser):
    check_instructor_course(request.course_id, db, current_instructor)

    new_module = Module(
        name = request.name,
        description = request.description,
        course_id = request.course_id
    )
    db.add(new_module)
    db.commit()
    db.refresh(new_module)

    return new_module


def update_module(id: int, request: ModuleUpdate, db: Session, current_instructor: CurrentUser):
    module = db.query(Module).filter(Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {id}")
    
    check_instructor_course(module.course_id, db, current_instructor)
    
    module.name = request.name
    module.description = request.description
    
    db.commit()
    db.refresh(module)

    return module


def delete_module(id: int, db: Session, current_instructor: CurrentUser):
    module = db.query(Module).filter(Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {id}")
    
    check_instructor_course(module.course_id, db, current_instructor)
    
    db.delete(module)
    db.commit()

    return None