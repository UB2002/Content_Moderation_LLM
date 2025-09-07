from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
from datetime import datetime


class ModerationRequest(Base):
    __tablename__ = "moderation_request"
    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String, nullable=False)
    content_hash = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(String,default="pending", nullable=False)
    created_time = Column(DateTime, default=datetime.utcnow, nullable=False)

    results = relationship("ModerationResult", back_populates="request")

class ModerationResult(Base):
    __tablename__ = "moderation_result"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("moderation_request.id"), nullable=False)
    classification = Column(String, nullable=False)
    confidence = Column(String, nullable=False)
    reasoning = Column(String, nullable=False)
    llm_response = Column(String, nullable=False)

    request = relationship("ModerationRequest", back_populates="results")