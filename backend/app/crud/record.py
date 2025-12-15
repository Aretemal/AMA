from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate


def get_record(db: Session, record_id: int) -> Optional[Record]:
    return db.query(Record).filter(Record.id == record_id).first()


def get_records(db: Session, skip: int = 0, limit: int = 100) -> List[Record]:
    return db.query(Record).offset(skip).limit(limit).all()


def get_records_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Record]:
    """Получить записи конкретного пользователя"""
    return db.query(Record).filter(Record.user_id == user_id).offset(skip).limit(limit).all()


def create_record(db: Session, record_in: RecordCreate, user_id: int) -> Record:
    """Создать запись с привязкой к пользователю"""
    record_data = record_in.model_dump()
    record_data["user_id"] = user_id
    db_record = Record(**record_data)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def update_record(db: Session, db_record: Record, record_in: RecordUpdate) -> Record:
    data = record_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_record, field, value)
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_record(db: Session, db_record: Record) -> None:
    db.delete(db_record)
    db.commit()
