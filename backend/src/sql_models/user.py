from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import bcrypt
import uuid
from sqlalchemy.dialects.postgresql import UUID
from ..models import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(80), unique=True, nullable=False)
    display_name = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    github_id = Column(String(255), unique=True, nullable=True)
    github_username = Column(String(255), nullable=True)
    
    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='author')

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
