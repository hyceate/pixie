from sqlalchemy import Column, String, UUID, DateTime
import uuid
from datetime import datetime
from ..models import Base

class Session(Base):
    __tablename__ = 'sessions'
    
    token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime)
