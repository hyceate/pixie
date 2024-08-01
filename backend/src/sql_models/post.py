from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..models import Base

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    author = relationship('User', back_populates='posts')
    
    comments = relationship('Comment', back_populates='post')
    images = relationship('Images', back_populates='post')
