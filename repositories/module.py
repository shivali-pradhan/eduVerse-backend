from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models.course_models import Module
from schemas.request_schemas import ModuleCreate, ModuleUpdate




def add_module(request: ModuleCreate, db: Session):
    # check_course(i_id, c_id, db)

    new_module = Module(
        name = request.name,
        description = request.description,
        created_at = datetime.datetime.now(),
        course_id = request.course_id
    )

    db.add(new_module)
    db.commit()
    db.refresh(new_module)

    return new_module

def update_module(id: int, request: ModuleCreate, db: Session):
    # check_course(i_id, c_id, db)

    # module = db.query(Module).filter(Module.id == id).first()
    # if not module:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such module with id: {m_id} in course with id: {c_id}")
    
    # module.name = request.name
    # module.description = request.description
    
    # db.commit()
    # db.refresh(module)

    # return module

    pass


def delete_module(i_id: int, c_id: int, m_id: int, db: Session):
    # check_course(i_id, c_id, db)

    # module = db.query(Module).filter(Module.id == m_id, Module.course_id == c_id)
    # if not module.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such module with id: {m_id} in course with id: {c_id}")
    
    # module.delete(synchronize_session=False)
    # db.commit()

    # return "deleted"
    pass