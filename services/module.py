from fastapi import HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
import os
from models.course_models import Module, LearningContentFile, Enrollment
from schemas.request_schemas import ModuleCreate, ModuleUpdate
from schemas.token_schemas import CurrentUser
from .course import check_instructor_course


def add_module(request: ModuleCreate, db: Session, current_instructor: CurrentUser):
    course = check_instructor_course(request.course_id, db, current_instructor)

    new_module = Module(
        name = request.name,
        description = request.description,
        duration = request.duration,
        course_id = request.course_id
    )
    
    db.add(new_module)
    db.flush()
    course.duration += new_module.duration

    db.commit()
    db.refresh(new_module)

    return new_module


def update_module(id: int, request: ModuleUpdate, db: Session, current_instructor: CurrentUser):
    module = db.query(Module).filter(Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {id}")
    
    course = check_instructor_course(module.course_id, db, current_instructor)
    
    course.duration -= module.duration

    module.name = request.name
    module.description = request.description
    module.duration = request.duration

    course.duration += request.duration
    
    db.commit()
    db.refresh(module)

    return module


def delete_module(id: int, db: Session, current_instructor: CurrentUser):
    module = db.query(Module).filter(Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {id}")
    
    course = check_instructor_course(module.course_id, db, current_instructor)
    
    db.delete(module)
    course.duration -= module.duration
    db.commit()

    return None

def get_module(id: int, db: Session, current_user: CurrentUser):
    module = db.query(Module).filter(Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {id}")
    
    if current_user.role == "STUDENT":
        course_enrollment = db.query(Enrollment).filter(Enrollment.course_id == module.course_id).first()
        if not course_enrollment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course not enrolled")
    
    return module

def save_file(id: int, db: Session, current_instructor: CurrentUser, file: UploadFile):
    module = db.query(Module).filter(Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {id}")
    
    check_instructor_course(module.course_id, db, current_instructor)
    
    ALLOWED_FILE_TYPES = ["application/pdf", "image/jpeg", "text/plain"]
    UPLOAD_DIR = "static"

    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"File type {file.content_type} not allowed. Allowed types are {ALLOWED_FILE_TYPES}")
    
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        content = file.file.read()

        with open(file_location, "wb") as f:
            f.write(content)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": "Error uploading this file", "error": str(e)})

    finally:
        new_content = LearningContentFile(
            file_name = file.filename,
            file_url = file_location,
            file_type = file.content_type,
            module_id = module.id
        )
        db.add(new_content)
        db.commit()

    return { "filename": file.filename, "file-content-length": len(content), "type": file.content_type }