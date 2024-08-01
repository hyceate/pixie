from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..models import Base

class Images(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255))
    post_id = Column(Integer, ForeignKey('posts.id'))
    
    post = relationship('Post', back_populates='images')
