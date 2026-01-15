from fastapi import APIRouter, UploadFile, Form, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..excel_importer import process_excel_file 
import shutil
import os


router = APIRouter(prefix="/import", tags=["import"])

UPLOAD_DIR = "uploads/excel"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("")
def import_excel(ministry_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Accept only excel mime types loosely
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Please upload an Excel file (.xlsx/ .xls)")
    
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        process_excel_file(db, filepath, ministry_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"import failed: {e}")

    return {"status": "ok", "imported": file.filename}