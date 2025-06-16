from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str 
    
class TokenData(BaseModel):
    email: str 
    
class StudentBase(BaseModel):
    full_name: str
    email: EmailStr
    is_active: Optional[int] = 0  # 1 for active, 0 for inactive
    is_admin: Optional[int] = 0  # 1 for admin, 0 for regular user
    supervisor_id: Optional[int] = None
    memory_master_id: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "johndoe@example.com"
            }
        }

class StudentLogin(BaseModel):
    email: EmailStr
    password: str
        
class StudentCreate(StudentBase):
    password: str

class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True
        
class StudentUpdate(StudentBase):
    pass 

class SupervisorBase(BaseModel):
    full_name: str
    speciality: str
    
class SupervisorCreate(SupervisorBase):
    pass

class Supervisor(SupervisorBase):
    availability: int
    id: int

    class Config:
        orm_mode = True
        
class SupervisorUpdate(SupervisorBase):
    pass
        
class MemoryMasterBase(BaseModel):
    full_name: str
    speciality: str
    
class MemoryMasterCreate(MemoryMasterBase):
    pass

class MemoryMaster(MemoryMasterBase):
    availability: bool 
    id: int

    class Config:
        orm_mode = True
        
class MemoryMasterUpdate(MemoryMasterBase):
    pass
        
    

