from datetime import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..models import Base

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime)
    
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    parent_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
    parent = relationship('Comment', remote_side=[id], back_populates='replies')
    replies = relationship('Comment', back_populates='parent')
