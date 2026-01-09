import logging

from fastapi import APIRouter, HTTPException
from app.workers.inference_worker import inference_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
def health_check():
    return {"status": "alive"}

@router.get("/ready")
def readiness():
    if inference_service is None:
        raise HTTPException(status_code=503, detail="Model not ready")
    
    logger.info("Readiness probe OK")
    return {"status": "ready"}