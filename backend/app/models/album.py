from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base

user_album_association = Table(
    'user_album',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('album_id', Integer, ForeignKey('albums.id'), primary_key=True)
)


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    
    title = Column(String(255), nullable=True)
    creator = Column(String(255), nullable=True)
    
    songs = relationship("Song", back_populates="album")
    users = relationship("User", secondary=user_album_association, back_populates="albums")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

