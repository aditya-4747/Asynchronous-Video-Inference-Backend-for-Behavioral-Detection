from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String, primary_key=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, index=True)
    video_key = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())