import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from .crud import get_or_create_department, create_staff
from .models import Ministry, Staff


# def process_excel_file(db: Session, filepath: str):
#     raw = pd.read_excel(filepath, engine="openpyxl", header=None)
    
#     print("\n==== RAW EXCEL PREVIEW ====\n")
#     print(raw.head(2))
#     print("\n==== RAW SHAPE ====\n")
#     print(raw.shape)
#     print("\n==== COLUMN SAMPLE ROWS ====\n")
#     for i in range(min(15, len(raw))):
#         print(f"Row {i}:", list(raw.iloc[i]))
        
#     raise RuntimeError("Debug stop - inspect printed Excel preview")

# REQUIRED_COLUMNS = {"ministry", "department", "full name"}

def process_excel_file(db: Session, filepath: str, ministry_id: int):
    
    def clean_str(val):
        if pd.isna(val):
            return None
        return str(val).strip()
    
    def clean_date(val):
        if pd.isna(val):
            return None
        if isinstance(val, pd.Timestamp):
            return val.date()
        # if isinstance(val, datetime):
        #     return val
        return None
    
    def clean_phone(val):
        if pd.isna(val):
            return None
        # Excel often reads numbers as floats: 
        try:
            return str(int(val))
        except Exception:
            return str(val).strip()
        
        
    df = pd.read_excel(filepath)

    ministry = db.query(Ministry).get(ministry_id)
    if not ministry:
        raise ValueError(f"Ministry with id {ministry_id} not found.")
    
    # HARD REFRESH -- delete existing staff for this ministry
    db.query(Staff).filter(
        Staff.department.has(ministry_id=ministry_id)
    ).delete(synchronize_session=False)
    db.commit()
    
    
    # Iterate rows
    for _, row in df.iterrows():
        dept_name = clean_str(row.get("Department"))
        full_name = clean_str(row.get("Full Name"))
        
        # Skip rows with missing required data
        if not dept_name or not full_name:
            continue
        
        photo = clean_str(row.get("Photo"))
        gender = clean_str(row.get("Sex"))
        rank = clean_str(row.get("Rank"))
        level = clean_str(row.get("SGL"))
        post = clean_str(row.get("Post"))
        first_appointment = clean_date(row.get("Appointment"))
        retirement = clean_date(row.get("Retirement"))
        native = clean_str(row.get("LGA"))
        phone_num = clean_phone(row.get("Number"))
        
        department = get_or_create_department(db, ministry, dept_name)
        
        create_staff(db, department, full_name, photo, gender, rank, level, post, first_appointment, retirement, native, phone_num)