from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class Ministry(Base):
    __tablename__ = "ministries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    # relationships
    departments = relationship("Department", back_populates="ministry")
    
    
class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ministry_id = Column(Integer, ForeignKey("ministries.id"), nullable=False)
    
    __table_args__ = (
        UniqueConstraint("ministry_id", "name", name="uq_ministry_department"),
    )
    # relationships
    ministry = relationship("Ministry", back_populates="departments")
    staff = relationship("Staff", back_populates="department")
    

class Staff(Base):
    __tablename__ = "staff"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    staff_id = Column(String, unique=True, nullable=False)
    photo = Column(String)
    gender = Column(String)
    rank = Column(String)
    level = Column(String)
    post = Column(String)
    first_appointment = Column(String)
    retirement = Column(String)
    native = Column(String)
    phone_num = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    
    department = relationship("Department", back_populates="staff")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())