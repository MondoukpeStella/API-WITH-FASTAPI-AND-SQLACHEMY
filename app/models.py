from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from typing import List

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str]  = mapped_column(String)
    is_active: Mapped[int] = mapped_column(Integer, default=1)  # 1 for active, 0 for inactive
    is_admin: Mapped[int] = mapped_column(Integer, default=0)  # 1 for admin, 0 for regular user
    supervisor_id: Mapped[int] = mapped_column(ForeignKey("supervisors.id"), nullable=True)
    memory_master_id: Mapped[int] = mapped_column(ForeignKey("memory_masters.id"), nullable=True)
    supervisor: Mapped["Supervisor"] = relationship("Supervisor", back_populates="students")
    memory_master: Mapped["MemoryMaster"] = relationship("MemoryMaster", back_populates="students")
    
class Supervisor(Base):
    __tablename__ = "supervisors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String, index=True)
    speciality: Mapped[str] = mapped_column(String, nullable=False)
    availability: Mapped[int] = mapped_column(Integer, default=3)  
    students: Mapped[List["Student"]] = relationship("Student", back_populates="supervisor")
    
class MemoryMaster(Base):
    __tablename__ = "memory_masters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String, index=True)
    speciality: Mapped[str] = mapped_column(String, nullable=False)
    availability: Mapped[bool] = mapped_column(Boolean, default=True)
    students: Mapped[List["Student"]] = relationship("Student", back_populates="memory_master")