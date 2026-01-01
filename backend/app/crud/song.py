import os
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.song import Song
from app.models.user import User
from app.schemas.song import SongCreate, SongUpdate


def get_songs(db: Session, skip: int = 0, limit: int = 100) -> List[Song]:
    return db.query(Song).offset(skip).limit(limit).all()


def get_songs_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Song]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
        
    return user.songs[skip:skip + limit] if user.songs else []


def save_uploaded_file(file: UploadFile, upload_dir: Path) -> str:
    file_extension = Path(file.filename).suffix if file.filename else ""
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / unique_filename
    
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    return unique_filename


def create_song(
    db: Session,
    file: UploadFile,
    user: User,
    title: Optional[str] = None,
    artist: Optional[str] = None,
    playlist: Optional[str] = None,
    album: Optional[str] = None,
) -> Song:
    upload_dir = Path(settings.UPLOAD_DIR)
    
    file_path = save_uploaded_file(file, upload_dir)
    
    db_song = Song(
        src=file_path,
        title=title,
        artist=artist,
        playlist=playlist,
        album=album,
    )
    
    db_song.users.append(user)
    
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    
    return db_song

def get_song(db: Session, song_id: int) -> Optional[Song]:
    return db.query(Song).filter(Song.id == song_id).first()


def get_songs_by_album(db: Session, album_id: int) -> List[Song]:
    return db.query(Song).filter(Song.album_id == album_id).all()