from fastapi import APIRouter, BackgroundTasks, HTTPException, File, UploadFile
import logging

from app.services import job_service
from app.workers.inference_worker import process_job
from app.services.job_service import storage

router = APIRouter(prefix="/jobs", tags=["jobs"])
logger = logging.getLogger(__name__)

@router.post("/create")
def create_job(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    job = job_service.create_job(file.file, file.filename)
    background_tasks.add_task(process_job, job.job_id)

    return job


@router.get("/{job_id}")
def get_job(job_id: str):
    job = job_service.get_job(job_id)
    if not job:
        logger.warning("Job not found", extra={"job_id": job_id})
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/{job_id}/result")
def get_result(job_id: str):
    result = job_service.get_job_result(job_id)
    if not result:
        logger.warning("Result not found", extra={"job_id": job_id})
        raise HTTPException(status_code=404, detail="Result not found")
    
    for det in result.detections:
        det.frame_key = storage.get_access_url(det.frame_key)

    return result