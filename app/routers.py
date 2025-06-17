from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from crud import auth, students, supervisors, memory_masters
from schemas import Token, StudentLogin, Student, StudentCreate, StudentUpdate, Supervisor, SupervisorCreate, SupervisorUpdate, MemoryMaster, MemoryMasterCreate, MemoryMasterUpdate
from crud.auth import JWTBearer

router = APIRouter()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@router.post("/register/", response_model=Student, tags=["User Registration"])
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    response = students.create(db, student)
    return response

@router.post("/login/", response_model=Token, tags=["User Registration"])
def login_student(student: StudentLogin, db: Session = Depends(get_db)):
    response = students.login(db, student)
    if response is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return auth.sign_jwt(response.id)

@router.get("/students/me", response_model=Student, tags=["User Registration"])
def get_my_profile(db: Session = Depends(get_db),student_id: int = Depends(auth.get_current_user_id)):
    student = students.get(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
        
@router.get("/students/", response_model=list[Student], dependencies=[Depends(JWTBearer())], tags=["Students"])
def get_all_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),student_id: int = Depends(auth.get_current_user_id)):
    user = students.get(db, student_id)
    if user.is_admin == 0:
        raise HTTPException(status_code=403, detail="Access forbidden: Only admins can view all students")
    response = students.get_all(db, skip=skip, limit=limit)
    return response

@router.get("/students/{student_id}", response_model=Student, dependencies=[Depends(JWTBearer())], tags=["Students"])
def read_student(student_id: int, db: Session = Depends(get_db)):
    response = students.get(db, student_id)
    return response

@router.put("/students/{student_id}", response_model=Student, dependencies=[Depends(JWTBearer())], tags=["Students"])
def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    response = students.update(db, student_id, student_update)
    if response is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return response

@router.delete("/students/{student_id}", response_model=Student, dependencies=[Depends(JWTBearer())], tags=["Students"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    response = students.delete(db, student_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return response

@router.post("/students/me/choose_supervisor/{supervisor_id}", response_model=Student, dependencies=[Depends(JWTBearer())], tags=["Students"])
def choose_supervisor(supervisor_id: int, student_id: int = Depends(auth.get_current_user_id), db: Session = Depends(get_db)):
    response = students.choose_supervisor(db, student_id, supervisor_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Student or Supervisor not found")
    return response

@router.post("/students/me/choose_memory_master/{memory_master_id}", response_model=Student, dependencies=[Depends(JWTBearer())], tags=["Students"])
def choose_memory_master(memory_master_id: int, student_id: int = Depends(auth.get_current_user_id), db: Session = Depends(get_db)):
    response = students.choose_memory_master(db, student_id, memory_master_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Student or Memory Master not found")
    return response

@router.put("/students/me/change_memory_master/{memory_master_id}", response_model=Student, dependencies=[Depends(JWTBearer())], tags=["Students"])
def change_memory_master(memory_master_id: int, student_id: int = Depends(auth.get_current_user_id), db: Session = Depends(get_db)):
    response = students.change_memory_master(db, student_id, memory_master_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Student or Memory Master not found")
    return response

@router.get("/supervisors/", response_model=list[Supervisor], dependencies=[Depends(JWTBearer())], tags=["Supervisors"])
def get_all_supervisors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    response = supervisors.get_all(db, skip=skip, limit=limit)
    return response

@router.post("/supervisors/", response_model=Supervisor, dependencies=[Depends(JWTBearer())], tags=["Supervisors"])
def create_supervisor(supervisor: SupervisorCreate, db: Session = Depends(get_db)):
    response = supervisors.create(db, supervisor)
    return response

@router.get("/supervisors/{supervisor_id}", response_model=Supervisor, dependencies=[Depends(JWTBearer())], tags=["Supervisors"])
def read_supervisor(supervisor_id: int, db: Session = Depends(get_db)):
    response = supervisors.get(db, supervisor_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    return response

@router.put("/supervisors/{supervisor_id}", response_model=Supervisor, dependencies=[Depends(JWTBearer())], tags=["Supervisors"])
def update_supervisor(supervisor_id: int, supervisor_update: supervisors.SupervisorUpdate, db: Session = Depends(get_db)):
    response = supervisors.update(db, supervisor_id, supervisor_update)
    if response is None:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    return response

@router.delete("/supervisors/{supervisor_id}", response_model=Supervisor, dependencies=[Depends(JWTBearer())], tags=["Supervisors"])
def delete_supervisor(supervisor_id: int, db: Session = Depends(get_db)):
    response = supervisors.delete(db, supervisor_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Supervisor not found")
    return response

@router.get("/memory_masters/", response_model=list[MemoryMaster], dependencies=[Depends(JWTBearer())], tags=["Memory Masters"])
def get_all_memory_masters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    response = memory_masters.get_all(db, skip=skip, limit=limit)
    return response

@router.post("/memory_masters/", response_model=MemoryMaster, dependencies=[Depends(JWTBearer())], tags=["Memory Masters"])
def create_memory_master(memory_master: MemoryMasterCreate, db: Session = Depends(get_db)):
    response = memory_masters.create(db, memory_master)
    return response

@router.get("/memory_masters/{memory_master_id}", response_model=MemoryMaster, dependencies=[Depends(JWTBearer())], tags=["Memory Masters"])
def read_memory_master(memory_master_id: int, db: Session = Depends(get_db)):
    response = memory_masters.get(db, memory_master_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Memory Master not found")
    return response

@router.put("/memory_masters/{memory_master_id}", response_model=MemoryMaster, dependencies=[Depends(JWTBearer())], tags=["Memory Masters"])
def update_memory_master(memory_master_id: int, memory_master_update: MemoryMasterUpdate, db: Session = Depends(get_db)):
    response = memory_masters.update(db, memory_master_id, memory_master_update)
    if response is None:
        raise HTTPException(status_code=404, detail="Memory Master not found")
    return response

@router.delete("/memory_masters/{memory_master_id}", response_model=MemoryMaster, dependencies=[Depends(JWTBearer())], tags=["Memory Masters"])
def delete_memory_master(memory_master_id: int, db: Session = Depends(get_db)):
    response = memory_masters.delete(db, memory_master_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Memory Master not found")
    return response


# Admin routes for choosing supervisors and memory masters to a student
# @router.post("/students/{student_id}/choose_supervisor/{supervisor_id}", response_model=Student, dependencies=[Depends(JWTBearer())], tags=["Admin"])
# def choose_supervisor(student_id: int, supervisor_id: int, db: Session = Depends(get_db)):
#     response = students.choose_supervisor(db, student_id, supervisor_id)
#     if response is None:
#         raise HTTPException(status_code=404, detail="Student or Supervisor not found")
#     return response

# @router.post("/students/{student_id}/choose_memory_master/{memory_master_id}", response_model=Student, dependencies=[Depends(JWTBearer())], tags=["Admin"])
# def choose_memory_master(student_id: int, memory_master_id: int, db: Session = Depends(get_db)):
#     response = students.choose_memory_master(db, student_id, memory_master_id)
#     if response is None:
#         raise HTTPException(status_code=404, detail="Student or Memory Master not found")
#     return response

# @router.put("/students/{student_id}/change_memory_master/{memory_master_id}", response_model=Student, dependencies=[Depends(JWTBearer())], tags=["Admin"])
# def change_memory_master(student_id: int, memory_master_id: int, db: Session = Depends(get_db)):
#     response = students.change_memory_master(db, student_id, memory_master_id)
#     if response is None:
#         raise HTTPException(status_code=404, detail="Student or Memory Master not found")
#     return response

