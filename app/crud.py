from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from .models import Ministry, Department, Staff


# ---------- Ministry -------------

def get_ministry_by_id(db: Session, ministry_id: int):
    return db.query(Ministry).filter(
        Ministry.id == ministry_id
        ).first()
    
    
# def get_ministries_paginated(db: Session, offset: int, limit: int):
#     items = db.query(Ministry).offset(offset).limit(limit).all()
#     total = db.query(Ministry).count()
#     return items, total


def get_ministries_paginated(db: Session, offset: int, limit: int):
    q = (
        db.query(
            Ministry,
            func.count(Staff.id).label("staff_count")
        )
        .outerjoin(Department, Department.ministry_id == Ministry.id)
        .outerjoin(Staff, Staff.department_id == Department.id)
        .group_by(Ministry.id)
    )
    
    items = q.offset(offset).limit(limit).all()
    total = q.count()
    
    results = []
    for ministry, staff_count in items:
        ministry.staff_count = staff_count
        results.append(ministry)
    
    return results, total


# ---------- Department -------------

# def get_department_by_id(db: Session, ministry_id: int, department_id: int):
#     return db.query(Department).filter(
#         Department.id == department_id,
#         Department.ministry_id == ministry_id
#         ).first()


def get_or_create_department(db: Session, ministry, name: str):
    dept = db.query(Department).filter(
        Department.ministry_id == ministry.id,
        Department.name == name,
    ).first()
    
    if dept:
        return dept # Reuse it
    
    dept = Department(name=name, ministry_id=ministry.id)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


def get_departments_paginated(
    db: Session, ministry_id: int, offset: int, limit: int):
    q = (
        db.query(
            Department,
            func.count(Staff.id).label("staff_count")
        )
        .outerjoin(Staff, Staff.department_id == Department.id)
        .filter(Department.ministry_id == ministry_id)
        .group_by(Department.id)
    )
    
    items = q.offset(offset).limit(limit).all()
    total = q.count()
    
    # unwrap tuples into dict-friendly objects
    results = []
    for dept, staff_count in items:
        dept.staff_count = staff_count
        results.append(dept)
    
    return results, total


# ---------- Staff -------------

def create_staff(
    db: Session, department, full_name, photo=None, gender=None, rank=None, level=None, post=None, first_appointment=None, retirement=None, native=None, phone_num=None):
    staff = Staff(
    full_name = full_name,
    photo = photo,
    gender = gender,
    rank = rank,
    level = level,
    post = post,
    first_appointment = first_appointment,
    retirement = retirement,
    native = native,
    phone_num = phone_num,
    department_id = department.id,
    )
    db.add(staff)     
    db.commit()
    db.refresh(staff)
    
    return staff


def get_staff_paginated(
    db: Session, 
    ministry_id: int, 
    department_id: int, 
    search: str | None, 
    rank: str | None, 
    offset: int, 
    limit: int
):
    q = (
        db.query(Staff)
        .join(Department, Staff.department_id == Department.id)
        .filter(
            Staff.department_id == department_id,
            Department.ministry_id == ministry_id
        )
    )
    
    if search is not None:
        search = search.strip()
        if search == "":
            q = q.filter()
        else:
            q = q.filter(Staff.full_name.ilike(f"%{search}%"))
        
    if rank is not None:
        q = q.filter(Staff.rank == rank)
        
    items = q.offset(offset).limit(limit).all()
    total = q.count()
    
    return items, total
    