from app.core.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float

class Frame(Base):
    __tablename__ = "frames"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, ForeignKey("jobs.job_id", ondelete="CASCADE"))
    frame_key = Column(String, nullable=False)
    timestamp = Column(Float, nullable=False)