from fastapi import APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from app.services import job_service
from app.services import result_service
from app.core.redis_client import redis_client
from app.core.config import QUEUE_NAME

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/create")
def create_job(file: UploadFile = File(...)):
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded")
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename")
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Only video files are allowed")
    
    job = job_service.create_job(file.file, file.filename)

    redis_client.lpush(QUEUE_NAME, job.job_id)
    return job


@router.get("/{job_id}")
def get_job(job_id: str):
    job = job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/{job_id}/result/raw")
def get_result(job_id: str):
    result = result_service.get_job_result(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return result


@router.get("/{job_id}/result/preview")
def get_result_preview(job_id: str):
    zip_path, temp_folder = result_service.generate_preview(job_id)

    if zip_path == "" or temp_folder == "":
        raise HTTPException(status_code=404, detail="Result not found")
    
    return FileResponse(
        zip_path, 
        filename=f"{job_id}_results.zip", 
        media_type="application/zip",
        background=BackgroundTask(result_service.cleanup_temp_files, zip_path, temp_folder)
    )