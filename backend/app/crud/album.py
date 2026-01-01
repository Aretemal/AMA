from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.album import Album
from app.models.song import Song
from app.models.user import User
from app.schemas.album import AlbumCreate, AlbumUpdate


def get_album(db: Session, album_id: int) -> Optional[Album]:
    return db.query(Album).filter(Album.id == album_id).first()


def get_albums(db: Session, skip: int = 0, limit: int = 100) -> List[Album]:
    return db.query(Album).offset(skip).limit(limit).all()


def get_albums_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Album]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    return user.albums[skip:skip + limit] if user.albums else []


def create_album(db: Session, album_in: AlbumCreate, user_id: int) -> Album:
    album_data = album_in.model_dump(exclude={"song_ids"})
    
    db_album = Album(**album_data)
    
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db_album.users.append(user)
    
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    
    if album_in.song_ids:
        songs = db.query(Song).filter(Song.id.in_(album_in.song_ids)).all()
        for song in songs:
            song.album_id = db_album.id
        db.commit()
    
    return db_album

def update_album(db: Session, db_album: Album, album_in: AlbumUpdate) -> Album:
    data = album_in.model_dump(exclude_unset=True, exclude={"song_ids"})
    
    for field, value in data.items():
        setattr(db_album, field, value)
    
    if album_in.song_ids is not None:
        for song in db_album.songs:
            song.album_id = None
        
        if album_in.song_ids:
            songs = db.query(Song).filter(Song.id.in_(album_in.song_ids)).all()
            for song in songs:
                song.album_id = db_album.id
    
    db.commit()
    db.refresh(db_album)
    return db_album

def delete_album(db: Session, db_album: Album) -> None:
    db.delete(db_album)
    db.commit()