from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    article = relationship("Article", backref="records")
    user = relationship("User", backref="records")
    
    content = Column(Text, nullable=True)
    type_record = Column(String(255), nullable=True)
    options = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    