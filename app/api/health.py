import logging
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
def health_check():
    return {"status": "alive"}

@router.get("/ready")
def readiness():
    return {"status": "ready"}