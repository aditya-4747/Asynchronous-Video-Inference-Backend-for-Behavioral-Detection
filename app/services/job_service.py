import uuid
from typing import Optional
import logging

from app.core.database import SessionLocal
from app.models.job import JobStatus, Job
from app.storage.local import LocalStorageService

storage = LocalStorageService()
logger = logging.getLogger(__name__)


def create_job(file, filename: str) -> Job:
    db = SessionLocal()

    try:
        job_id = str(uuid.uuid4())
        video_path = storage.upload_video(file, filename)

        job = Job(job_id=job_id, video_key=video_path)
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