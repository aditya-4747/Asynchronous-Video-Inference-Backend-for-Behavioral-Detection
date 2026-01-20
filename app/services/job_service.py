import uuid
from typing import Optional
import logging
import magic

from app.core.database import SessionLocal
from app.models.job import JobStatus, Job
from app.storage import get_storage_service

storage = get_storage_service()
logger = logging.getLogger(__name__)


def get_video_extension(file_bytes: bytes) -> str:
    mime = magic.from_buffer(file_bytes, mime=True)

    allowed_types = {
        "video/mp4": "mp4",
        "video/x-matroska": "mkv",
        "video/quicktime": "mov"
    }

    if mime not in allowed_types:
        raise ValueError("Unsupported file type")
    
    return allowed_types[mime]


def create_job(file, filename: str) -> Job:
    db = SessionLocal()

    try:
        job_id = str(uuid.uuid4())
        file_bytes = file.read()
        ext = get_video_extension(file_bytes)

        filename = f"{job_id}.{ext.lower()}"
        storage.upload_video(file_bytes, filename)

        job = Job(job_id=job_id, video_key=filename)
        db.add(job)
        db.commit()
        db.refresh(job)

        logger.info("Job created", extra={"job_id": job.job_id})
        return job
    
    finally:
        db.close()


def get_job(job_id: str) -> Optional[Job]:
    db = SessionLocal()
    try:
        return db.query(Job).filter(Job.job_id == job_id).first()

    finally:
        db.close()


def mark_job_processing(job_id: str) -> None:
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            return
        
        job.status = JobStatus.PROCESSING
        db.commit()

        logger.info("Job processing started", extra={"job_id": job_id})

    finally:
        db.close()


def mark_job_completed(job_id: str) -> None:
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            return
        
        job.status = JobStatus.COMPLETED
        db.commit()

        logger.info("Job completed", extra={"job_id": job_id})

    finally:
        db.close()


def mark_job_failed(job_id: str) -> None:
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.job_id == job_id).first()
        if not job:
            return
        
        job.status = JobStatus.FAILED
        db.commit()

        logger.info("Job failed", extra={"job_id": job_id})

    finally:
        db.close()


def reset_stuck_jobs():
    db = SessionLocal()

    try:
        stuck_jobs = db.query(Job).filter(Job.status == JobStatus.PROCESSING).all()

        for job in stuck_jobs:
            job.status = JobStatus.PENDING
        
        db.commit()

        if stuck_jobs:
            logger.warning(f"Reset {len(stuck_jobs)} stuck jobs to Pending state")
        
    finally:
        db.close()


def get_pending_jobs() -> list:
    db = SessionLocal()

    try:
        pending_jobs = db.query(Job).filter(Job.status == JobStatus.PENDING).all()
        return pending_jobs
    
    finally:
        db.close()