from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Student, Supervisor, MemoryMaster
from schemas import StudentLogin, StudentCreate, StudentUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# CRUD operations for Student
def get_all(db: Session, skip: int = 0, limit: int = 10) -> list[Student]:
    return db.query(Student).offset(skip).limit(limit).all()

def login(db: Session, student: StudentLogin) -> Student:
    db_student = db.query(Student).filter(Student.email == student.email).first()
    if not db_student :
        raise HTTPException(status_code=400, detail="Email is not registered")
    if not verify_password(student.password, db_student.hashed_password):
        raise HTTPException(status_code=401, detail="Password is incorrect")
    
    db_student.is_active = True  # Set the student as active upon login
    db.commit()
    db.refresh(db_student)
    return db_student

def create(db: Session, student: StudentCreate) -> Student:
    hashed_password = hash_password(student.password)
    db_student = Student(
        full_name=student.full_name,
        email=student.email,
        hashed_password=hashed_password,
        is_active=student.is_active,
        is_admin=student.is_admin,
        supervisor_id=student.supervisor_id,
        memory_master_id=student.memory_master_id
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get(db: Session, student_id: int) -> Student:
    return db.query(Student).filter(Student.id == student_id).first()

def update(db: Session, student_id: int, student_update: StudentUpdate) -> Student:
    pass

def delete(db: Session, student_id: int) -> Student:
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        return None
    db.delete(db_student)
    db.commit()
    return db_student

def choose_supervisor(db: Session, student_id: int, supervisor_id: int) -> Student:
    db_student = db.query(Student).filter(Student.id == student_id).first()
    db_supervisor = db.query(Supervisor).filter(Supervisor.id == supervisor_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if db_student.supervisor_id == supervisor_id:
        raise HTTPException(status_code=400, detail="Supervisor already assigned to this student")
    
    if db_supervisor.availability <= 0:
        raise HTTPException(status_code=400, detail="Supervisor is not available")
    
    db_supervisor.availability -= 1
    db_student.supervisor_id = supervisor_id
    db.commit()
    db.refresh(db_student)
    db.refresh(db_supervisor)
    return db_student

def choose_memory_master(db: Session, student_id: int, memory_master_id: int) -> Student:
    db_student = db.query(Student).filter(Student.id == student_id).first()
    db_memory_master = db.query(MemoryMaster).filter(MemoryMaster.id == memory_master_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if db_student.memory_master_id == memory_master_id:
        raise HTTPException(status_code=400, detail="Memory Master already assigned to this student")
    
    if not db_memory_master.availability:
        raise HTTPException(status_code=400, detail="Memory Master is not available")
    
    db_memory_master.availability = False
    db_student.memory_master_id = memory_master_id
    db.commit()
    db.refresh(db_student)
    db.refresh(db_memory_master)
    return db_student

def change_memory_master(db: Session, student_id: int, memory_master_id: int) -> Student:
    db_student = db.query(Student).filter(Student.id == student_id).first()
    db_memory_master = db.query(MemoryMaster).filter(MemoryMaster.id == memory_master_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if db_student.memory_master_id == memory_master_id:
        raise HTTPException(status_code=400, detail="Memory Master already assigned to this student")
    
    if not db_memory_master.availability:
        raise HTTPException(status_code=400, detail="Memory Master is not available")
    
    # Reset the previous Memory Master's availability
    if db_student.memory_master_id:
        previous_memory_master = db.query(MemoryMaster).filter(MemoryMaster.id == db_student.memory_master_id).first()
        previous_memory_master.availability = True
    
    db_memory_master.availability = False
    db_student.memory_master_id = memory_master_id
    db.commit()
    db.refresh(db_student)
    return db_student
