from pydantic import BaseModel
from typing import List


class Detection(BaseModel):
    timestamp: float
    confidence: float
    frame_key: str


class JobResult(BaseModel):
    job_id: str
    detections: List[Detection]