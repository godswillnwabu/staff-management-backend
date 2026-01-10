from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import ministries, import_router, departments, staff
# from sync import start_scheduler
from fastapi.staticfiles import StaticFiles


# AFTER models are imported, now create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nominal Directory")

# ----- CORS configuration -----
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    # add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/photos", StaticFiles(directory="uploads/photos"), name="photos")

app.include_router(import_router.router)
app.include_router(ministries.router)
app.include_router(departments.router)
app.include_router(staff.router)

# start_scheduler()