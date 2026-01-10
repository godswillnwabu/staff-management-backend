from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, crud


router = APIRouter(prefix="/ministries", tags=["Departments"])


# @router.get("/{ministry_id}/departments/{department_id}", response_model=schemas.DepartmentRead)
# def get_department(ministry_id: int, department_id: int, db: Session = Depends(get_db)):
#     d = crud.get_department_by_id(db, ministry_id=ministry_id, department_id=department_id)
#     if not d:
#         raise HTTPException(status_code=404, detail="Department not found")
#     return d


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
    
# @router.get("/{ministry_id}/departments", response_model=list[schemas.DepartmentRead])
# def list_departments(ministry_id: int, db: Session = Depends(get_db)):
#     return (
#         db.query(models.Department)
#         .filter(models.Department.ministry_id == ministry_id)
#         .all()
#     )