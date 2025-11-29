from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import record as record_crud
from app.db.session import get_db
from app.schemas.record import RecordCreate, RecordRead, RecordUpdate

router = APIRouter(prefix="/records", tags=["records"])


@router.get("/", response_model=list[RecordRead])
def list_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return record_crud.get_records(db, skip=skip, limit=limit)


@router.post("/", response_model=RecordRead, status_code=status.HTTP_201_CREATED)
def create_record(record_in: RecordCreate, db: Session = Depends(get_db)):
    return record_crud.create_record(db, record_in)


@router.get("/{record_id}", response_model=RecordRead)
def get_record(record_id: int, db: Session = Depends(get_db)):
    db_record = record_crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return db_record


@router.put("/{record_id}", response_model=RecordRead)
def update_record(record_id: int, record_in: RecordUpdate, db: Session = Depends(get_db)):
    db_record = record_crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record_crud.update_record(db, db_record, record_in)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    db_record = record_crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    record_crud.delete_record(db, db_record)