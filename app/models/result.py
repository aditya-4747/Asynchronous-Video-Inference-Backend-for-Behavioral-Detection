from pydantic import BaseModel
from typing import List

class SpittingInstance(BaseModel):
    conf: float
    box: List


class Detection(BaseModel):
    timestamp: float
    instances: List[SpittingInstance]
    frame_key: str


class JobResult(BaseModel):
    job_id: str
    detections: List[Detection]