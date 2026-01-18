import time
import logging

# Logging setup
from app.core.logging import setup_logging
setup_logging()

from app.core.redis_client import redis_client
from app.core.config import QUEUE_NAME
from app.workers.inference_worker import process_job

logger = logging.getLogger(__name__)

# Re-process stuck jobs
from app.services.job_service import reset_stuck_jobs, get_pending_jobs
reset_stuck_jobs()

for job in get_pending_jobs():
    redis_client.lpush(QUEUE_NAME, job.job_id)


def run_worker():
    logger.info("Worker started, looking for jobs...")

    while True:
        job = redis_client.blpop(QUEUE_NAME, timeout=5)

        if job:
            job_id = job[1]
            logger.info("Job dequeued", extra={"job_id": job_id})
            process_job(job_id)

        else:
            time.sleep(1)

if __name__ == "__main__":
    run_worker()