from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, crud


router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/{department_id}", response_model=schemas.DepartmentRead)
def get_department(department_id: int, db: Session = Depends(get_db)):
    d = crud.get_department_by_id(db, ministry=None, department_id=department_id)
    if not d:
        raise HTTPException(status_code=404, detail="Department not found")
    return d

# @router.get("/{department_id}/staff", response_model=list[schemas.StaffRead])
# def list_staff(department_id: int, db: Session = Depends(get_db)):
#     return (
#         db.query(models.Staff)
#         .filter(models.Staff.department_id == department_id)
#         .all()
#     )
    
    
@router.get("/{department_id}/staff", response_model=schemas.PaginatedStaff)
def paginated_staff(
    department_id: int,
    search: str | None = None,
    rank: str | None = None,
    page: int = 1,
    page_size: int = 6,
    db: Session = Depends(get_db)):
    
    offset = (page - 1) * page_size
    items, total = crud.get_staff_paginated(db, department_id, search, rank, offset, page_size)
    
    return { 
        "items": items, 
        "total": total, 
        "page": page, 
        "page_size": page_size 
    }