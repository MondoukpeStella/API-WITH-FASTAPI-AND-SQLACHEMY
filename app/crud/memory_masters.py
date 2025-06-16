from sqlalchemy.orm import Session
from models import MemoryMaster
from schemas import MemoryMasterBase, MemoryMasterCreate, MemoryMasterUpdate

def get_all(db: Session, skip: int = 0, limit: int = 10) -> list[MemoryMaster]:
    return db.query(MemoryMaster).offset(skip).limit(limit).all()

def create(db: Session, memory_master: MemoryMasterCreate) -> MemoryMaster:
    db_memory_master = MemoryMaster(
        full_name=memory_master.full_name,
        speciality=memory_master.speciality,
    )
    db.add(db_memory_master)
    db.commit()
    db.refresh(db_memory_master)
    return db_memory_master

def get(db: Session, memory_master_id: int) -> MemoryMaster:
    return db.query(MemoryMaster).filter(MemoryMaster.id == memory_master_id).first()

def update(db: Session, memory_master_id: int, memory_master_update: MemoryMasterUpdate) -> MemoryMaster:
    pass

def delete(db: Session, memory_master_id: int) -> MemoryMaster:
    db_memory_master = db.query(MemoryMaster).filter(MemoryMaster.id == memory_master_id).first()
    if not db_memory_master:
        return None
    db.delete(db_memory_master)
    db.commit()
    return db_memory_master