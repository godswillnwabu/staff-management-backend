from pydantic import BaseModel
from typing import List, Optional

    
class StaffRead(BaseModel):
    id: int
    full_name: str
    photo: Optional[str]
    gender: Optional[str]
    rank: Optional[str]
    level: Optional[str]
    post: Optional[str]
    first_appointment: Optional[str]
    retirement: Optional[str]
    native: Optional[str]
    phone_num: Optional[str]
    department: Optional["DepartmentRead"]
    
    model_config = {"from_attributes": True}
        
    
class DepartmentRead(BaseModel):
    id: int
    name: str
    staff_count: Optional[int] = None
    ministry: Optional["MinistryRead"]
    
    model_config = {"from_attributes": True}
        
    
class MinistryRead(BaseModel):
    id: int
    name: str
    staff_count: Optional[int] = None
    
    model_config = {"from_attributes": True} 
    
    
class MinistryCreate(BaseModel):
    name: str
    
    
class PaginatedBase(BaseModel):
    total: int
    page: int
    page_size: int
    
    
class PaginatedMinistries(PaginatedBase):
    items: List[MinistryRead]
    
    
class PaginatedDepartments(PaginatedBase):
    items: List[DepartmentRead]
    
    
class PaginatedStaff(PaginatedBase):
    items: List[StaffRead]