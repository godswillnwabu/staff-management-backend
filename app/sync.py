# import os
# from apscheduler.schedulers.background import BackgroundScheduler
# from database import SessionLocal
# from excel_importer import process_excel_file

# EXCEL_PATH = "uploads/excel"

# _last_mtime = None


# def sync_excel():
#     global _last_mtime
#     try:
#         mtime = os.path.getmtime(EXCEL_PATH)
#         if _last_mtime is None or mtime > _last_mtime:
#             print("Detected Excel change -- syncing...")
#             db = SessionLocal()
#             try:
#                 process_excel_file(db, EXCEL_PATH)
#             finally:
#                 db.close()
#             _last_mtime = mtime
#     except FileNotFoundError:
#         print("Excel file not found -- waiting...")
        
        
# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(sync_excel, "interval", minutes=10)
#     scheduler.start()