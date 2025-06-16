from sqlalchemy.orm import Session
from models import Supervisor
from schemas import SupervisorBase, SupervisorCreate, SupervisorUpdate

# CRUD operations for Supervisor
def get_all(db: Session, skip: int = 0, limit: int = 10) -> list[Supervisor]:
    return db.query(Supervisor).offset(skip).limit(limit).all()

def create(db: Session, supervisor: SupervisorCreate) -> Supervisor:
    db_supervisor = Supervisor(
        full_name=supervisor.full_name,
        speciality=supervisor.speciality,
    )
    db.add(db_supervisor)
    db.commit()
    db.refresh(db_supervisor)
    return db_supervisor

def get(db: Session, supervisor_id: int) -> Supervisor:
    return db.query(Supervisor).filter(Supervisor.id == supervisor_id).first()

def update(db: Session, supervisor_id: int, supervisor_update: SupervisorUpdate) -> Supervisor:
    pass

def delete(db: Session, supervisor_id: int) -> Supervisor:
    db_supervisor = db.query(Supervisor).filter(Supervisor.id == supervisor_id).first()
    if not db_supervisor:
        return None
    db.delete(db_supervisor)
    db.commit()
    return db_supervisor


