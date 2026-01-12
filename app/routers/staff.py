from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, crud


router = APIRouter(prefix="/ministries", tags=["Staff"])


@router.get("/{ministry_id}/departments/{department_id}/staff", response_model=schemas.PaginatedStaff)
def paginated_staff(
    ministry_id: int,
    department_id: int,
    page: int = 1,
    page_size: int = 6,
    search: str | None = None,
    rank: str | None = None,
    db: Session = Depends(get_db)
):
    # print("SEARCH:", repr(search), "RANK:", repr(rank))
    offset = (page - 1) * page_size
    
    items, total = crud.get_staff_paginated(
        db=db, 
        ministry_id=ministry_id,
        department_id=department_id, 
        search=search, 
        rank=rank, 
        offset=offset, 
        limit=page_size,
    )
    
    return { 
        "items": items, 
        "total": total, 
        "page": page, 
        "page_size": page_size 
    }
    
# @router.get("/{ministry_id}/departments/{department_id}/staff", response_model=list[schemas.StaffRead])
# def list_staff(department_id: int, db: Session = Depends(get_db)):
#     return (
#         db.query(models.Staff)
#         .filter(models.Staff.department_id == department_id)
#         .all()
#     )