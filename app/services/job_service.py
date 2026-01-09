import uuid
from datetime import datetime, UTC
from typing import Optional
import logging

from app.models.job import JobStatus, Job
from app.models.result import JobResult
from app.storage.local import LocalStorageService

_JOBS: dict[str, Job] = {}
_RESULTS: dict[str, JobResult] = {}

storage = LocalStorageService()
logger = logging.getLogger(__name__)


def _create_base_job() -> Job:
    job_id = str(uuid.uuid4())
    job = Job(
        job_id = job_id,
        status = JobStatus.PENDING,
        created_at = datetime.now(UTC)
    )

    _JOBS[job_id] = job
    return job


def create_job(file, filename: str) -> Job:
    job = _create_base_job()
    video_key = storage.upload_video(file, filename)
    job.video_key = video_key

    logger.info("Job created", extra={"job_id": job.job_id})
    return job


def get_job(job_id: str) -> Optional[Job]:
    return _JOBS.get(job_id)


def mark_job_processing(job_id: str) -> None:
    job = _JOBS.get(job_id)
    if job:
        job.status = JobStatus.PROCESSING
    
    logger.info("Job processing started", extra={"job_id": job_id})


def mark_job_completed(job_id: str) -> None:
    job = _JOBS.get(job_id)
    if job:
        job.status = JobStatus.COMPLETED

    logger.info("Job completed", extra={"job_id": job_id})


def mark_job_failed(job_id: str) -> None:
    job = _JOBS.get(job_id)
    if job:
        job.status = JobStatus.FAILED

    logger.error("Job failed", extra={"job_id": job_id}, exc_info=True)


def save_job_result(result: JobResult) -> None:
    _RESULTS[result.job_id] = result


def get_job_result(job_id: str) -> Optional[JobResult]:
    return _RESULTS.get(job_id)