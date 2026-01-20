import logging

# Logging setup
from app.core.logging import setup_logging
setup_logging()

from app.infrastructure.sqs_client import send_message, receive_messages, delete_message
from app.workers.inference_worker import process_job

logger = logging.getLogger(__name__)

# Re-process stuck jobs
from app.services.job_service import reset_stuck_jobs, get_pending_jobs
reset_stuck_jobs()

for job in get_pending_jobs():
    send_message(str(job.job_id))

logger.info("Queue ready. Looking for jobs...")

while True:
    messages = receive_messages()
    
    if not messages:
        continue

    for msg in messages:
        job_id = msg["Body"]
        receipt = msg["ReceiptHandle"]

        try:
            logger.info("Dequeued job", extra={"job_id": job_id})
            process_job(job_id)
            delete_message(receipt)

        except Exception as e:
            print(e)