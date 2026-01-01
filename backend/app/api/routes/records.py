from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_user_from_request, verify_auth_global
from app.crud import record as record_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.record import RecordCreate, RecordRead, RecordUpdate

router = APIRouter(
    prefix="/records",
    tags=["records"],
    dependencies=[Depends(verify_auth_global)],
)


@router.get("/", response_model=list[RecordRead])
def list_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    return record_crud.get_records_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=RecordRead, status_code=status.HTTP_201_CREATED)
def create_record(
    record_in: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    return record_crud.create_record(db, record_in, user_id=current_user.id)


@router.get("/{record_id}", response_model=RecordRead)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    db_record = record_crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    if db_record.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return db_record


@router.put("/{record_id}", response_model=RecordRead)
def update_record(
    record_id: int,
    record_in: RecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    db_record = record_crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    if db_record.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return record_crud.update_record(db, db_record, record_in)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    db_record = record_crud.get_record(db, record_id)
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    if db_record.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    record_crud.delete_record(db, db_record)