from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_user_from_request, verify_auth_global
from app.crud import album as album_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.album import AlbumCreate, AlbumRead, AlbumUpdate

router = APIRouter(
    prefix="/albums",
    tags=["albums"],
    dependencies=[Depends(verify_auth_global)],
)


@router.get("/", response_model=list[AlbumRead])
def list_albums(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    albums = album_crud.get_albums_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    
    result = []
    for album in albums:
        album_dict = {
            "id": album.id,
            "title": album.title,
            "creator": album.creator,
            "song_ids": [song.id for song in album.songs],
            "user_ids": [user.id for user in album.users],
            "created_at": album.created_at,
            "updated_at": album.updated_at,
        }
        result.append(AlbumRead(**album_dict))
    return result


@router.post("/", response_model=AlbumRead, status_code=status.HTTP_201_CREATED)
def create_album(
    album_in: AlbumCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    db_album = album_crud.create_album(db, album_in, user_id=current_user.id)
    
    return AlbumRead(
        id=db_album.id,
        title=db_album.title,
        creator=db_album.creator,
        song_ids=[song.id for song in db_album.songs],
        user_ids=[user.id for user in db_album.users],
        created_at=db_album.created_at,
        updated_at=db_album.updated_at,
    )


@router.get("/{album_id}", response_model=AlbumRead)
def get_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    db_album = album_crud.get_album(db, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    
    if current_user not in db_album.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    return AlbumRead(
        id=db_album.id,
        title=db_album.title,
        creator=db_album.creator,
        song_ids=[song.id for song in db_album.songs],
        user_ids=[user.id for user in db_album.users],
        created_at=db_album.created_at,
        updated_at=db_album.updated_at,
    )


@router.put("/{album_id}", response_model=AlbumRead)
def update_album(
    album_id: int,
    album_in: AlbumUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    db_album = album_crud.get_album(db, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    
    if current_user not in db_album.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    updated_album = album_crud.update_album(db, db_album, album_in)
    
    return AlbumRead(
        id=updated_album.id,
        title=updated_album.title,
        creator=updated_album.creator,
        song_ids=[song.id for song in updated_album.songs],
        user_ids=[user.id for user in updated_album.users],
        created_at=updated_album.created_at,
        updated_at=updated_album.updated_at,
    )


@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    db_album = album_crud.get_album(db, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    
    album_crud.delete_album(db, db_album)



