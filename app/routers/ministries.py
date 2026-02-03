from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..database import get_db
from app import crud
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


@router.get("", response_model=schemas.PaginatedMinistries)
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
    
    
@router.post("", response_model=schemas.MinistryRead)
def create_ministry(ministry: schemas.MinistryCreate, db: Session = Depends(get_db)):
    m = models.Ministry(name=ministry.name.strip())
    db.add(m)
    try:
        db.commit()
        db.refresh(m)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ministry name already exist."
        )
    return m


@router.put("/{ministry_id}", response_model=schemas.MinistryRead)
def update_ministry(
    ministry_id: int, 
    ministry_update: schemas.MinistryUpdate, 
    db: Session = Depends(get_db)
):
    m = crud.update_ministry_name_by_id(
        db, 
        ministry_id=ministry_id, 
        new_name=ministry_update.name.strip()
    )
    if not m:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ministry not found")
    return m


@router.delete("/{ministry_id}", response_model=schemas.MinistryRead)
def delete_ministry(ministry_id: int, db: Session = Depends(get_db)):
    m = crud.delete_ministry_by_id(db, ministry_id=ministry_id)
    if not m:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ministry not found")
    return m

    
    
