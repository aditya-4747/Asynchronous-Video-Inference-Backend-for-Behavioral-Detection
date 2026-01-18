from sqlalchemy import Column, Integer, ForeignKey, Float
from app.core.database import Base

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    frame_id = Column(Integer, ForeignKey("frames.id"), index=True)
    conf = Column(Float, nullable=False)
    x1 = Column(Float, nullable=False)
    y1 = Column(Float, nullable=False)
    x2 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)