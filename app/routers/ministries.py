from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from ..database import get_db
from .. import models, schemas


router = APIRouter(prefix="/ministries", tags=["Ministries"])


@router.get("/{ministry_id}", response_model=schemas.MinistryRead)
def get_ministry(ministry_id: int, db: Session = Depends(get_db)):
    m = crud.get_ministry_by_id(db, ministry_id)
    if not m:
        raise HTTPException(status_code=404, detail="Ministry not found")
    return m


# @router.get("/", response_model=list[schemas.MinistryRead])
# def list_ministries(db: Session = Depends(get_db)):
#     return db.query(models.Ministry).all()


@router.get("/", response_model=schemas.PaginatedMinistries)
def paginated_ministries(
    page: int = 1, 
    page_size: int = 12, 
    db: Session = Depends(get_db)):
    
    offset = (page - 1) * page_size
    items, total = crud.get_ministries_paginated(db, offset, page_size)
    
    return { 
        "items": items, 
        "total": total, 
        "page": page, 
        "page_size": page_size 
    }
    
    
@router.post("/", response_model=schemas.MinistryRead)
def create_ministry(ministry: schemas.MinistryCreate, db: Session = Depends(get_db)):
    m = models.Ministry(name=ministry.name)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


# @router.get("/{ministry_id}/departments", response_model=list[schemas.DepartmentRead])
# def list_departments(ministry_id: int, db: Session = Depends(get_db)):
#     return (
#         db.query(models.Department)
#         .filter(models.Department.ministry_id == ministry_id)
#         .all()
#     )
    
    
@router.get("/{ministry_id}/departments", response_model=schemas.PaginatedDepartments)
def paginated_departments(
    ministry_id: int, 
    page: int = 1, 
    page_size: int = 9, 
    db: Session = Depends(get_db)):
    
    offset = (page - 1) * page_size
    items, total = crud.get_departments_paginated(db, ministry_id, offset, page_size)
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size
    }