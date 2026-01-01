import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import get_user_from_request, verify_auth_global
from app.core.config import settings
from app.crud import song as song_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.song import SongRead, SongUpdate

router = APIRouter(
    prefix="/songs",
    tags=["songs"],
    dependencies=[Depends(verify_auth_global)],
)


@router.get("/", response_model=list[SongRead])
def list_songs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    songs = song_crud.get_songs_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    
    result = []
    for song in songs:
        album_name = song.album.title if song.album else None
        song_dict = {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "src": song.src,
            "playlist": song.playlist,
            "album": album_name,
            "user_ids": [user.id for user in song.users],
            "created_at": song.created_at,
            "updated_at": song.updated_at,
        }
        result.append(SongRead(**song_dict))
    return result


@router.post("/", response_model=SongRead, status_code=status.HTTP_201_CREATED)
def create_song(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    artist: Optional[str] = Form(None),
    playlist: Optional[str] = Form(None),
    album: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Файл должен быть аудио файлом"
        )
    
    song = song_crud.create_song(
        db=db,
        file=file,
        user=current_user,
        title=title,
        artist=artist,
        playlist=playlist,
        album=album,
    )
    
    album_name = song.album.title if song.album else None
    return SongRead(
        id=song.id,
        title=song.title,
        artist=song.artist,
        src=song.src,
        playlist=song.playlist,
        album=album_name,
        user_ids=[user.id for user in song.users],
        created_at=song.created_at,
        updated_at=song.updated_at,
    )

@router.get("/album/{album_id}", response_model=list[SongRead])
def get_songs_by_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    songs = song_crud.get_songs_by_album(db, album_id)
    return [SongRead(
        id=song.id, 
        title=song.title, 
        artist=song.artist, 
        src=song.src, playlist=song.playlist, 
        album=song.album.title, 
        user_ids=[user.id for user in song.users], 
        created_at=song.created_at, 
        updated_at=song.updated_at
        ) for song in songs]


@router.get("/{song_id}/stream")
async def stream_song(
    song_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_user_from_request),
):
    """
    Потоковая передача аудиофайла с поддержкой Range Requests.
    Позволяет начинать воспроизведение до полной загрузки файла.
    """
    # Получаем песню из БД
    song = song_crud.get_song(db, song_id)
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")
    
    # Проверяем доступ пользователя
    if current_user not in song.users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    # Формируем путь к файлу
    file_path = Path(settings.UPLOAD_DIR) / song.src
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    # Получаем размер файла
    file_size = file_path.stat().st_size
    
    # Обрабатываем Range Request
    range_header = request.headers.get("range")
    
    if range_header:
        # Парсим Range заголовок (формат: "bytes=start-end")
        range_match = range_header.replace("bytes=", "").split("-")
        start = int(range_match[0]) if range_match[0] else 0
        end = int(range_match[1]) if range_match[1] else file_size - 1
        
        # Ограничиваем end размером файла
        end = min(end, file_size - 1)
        
        # Вычисляем длину части
        content_length = end - start + 1
        
        # Читаем нужную часть файла
        def iterfile():
            with open(file_path, "rb") as file:
                file.seek(start)
                remaining = content_length
                while remaining:
                    chunk_size = min(8192, remaining)  # Читаем по 8KB
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk
        
        # Определяем Content-Type
        content_type = "audio/mpeg"  # По умолчанию MP3
        if song.src.endswith(".mp3"):
            content_type = "audio/mpeg"
        elif song.src.endswith(".wav"):
            content_type = "audio/wav"
        elif song.src.endswith(".ogg"):
            content_type = "audio/ogg"
        elif song.src.endswith(".m4a"):
            content_type = "audio/mp4"
        
        # Возвращаем частичный контент (206)
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            "Content-Type": content_type,
        }
        
        return StreamingResponse(
            iterfile(),
            status_code=206,
            headers=headers,
            media_type=content_type,
        )
    else:
        # Если Range не указан, возвращаем весь файл
        def iterfile():
            with open(file_path, "rb") as file:
                while True:
                    chunk = file.read(8192)  # Читаем по 8KB
                    if not chunk:
                        break
                    yield chunk
        
        # Определяем Content-Type
        content_type = "audio/mpeg"
        if song.src.endswith(".mp3"):
            content_type = "audio/mpeg"
        elif song.src.endswith(".wav"):
            content_type = "audio/wav"
        elif song.src.endswith(".ogg"):
            content_type = "audio/ogg"
        elif song.src.endswith(".m4a"):
            content_type = "audio/mp4"
        
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
            "Content-Type": content_type,
        }
        
        return StreamingResponse(
            iterfile(),
            status_code=200,
            headers=headers,
            media_type=content_type,
        )
