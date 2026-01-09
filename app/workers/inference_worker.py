import cv2
import logging

from app.services import job_service
from app.models.result import JobResult, Detection
from app.services.job_service import storage
from app.services.model_loader import ensure_model_present
from app.services.inference_service import YoloInferenceService
from app.core.config import FRAME_INTERVAL

MODEL_PATH = ensure_model_present()
inference_service = YoloInferenceService(MODEL_PATH)
logger = logging.getLogger(__name__)


def process_job(job_id: str):
    logger.info("Worker started job processing", extra={"job_id": job_id})

    try:
        job_service.mark_job_processing(job_id)

        job = job_service.get_job(job_id)
        video_path = storage.get_access_url(job.video_key)
        
        detections = inference_service.run(video_path, FRAME_INTERVAL)
        logger.info(
            "Inference completed", 
            extra={"job_id": job_id, "detections": len(detections)}
        )

        result_detections = []

        for idx, (timestamp, conf, frame) in enumerate(detections, start=1):
            success, buffer = cv2.imencode(".jpg", frame)
            if not success:
                continue

            frame_key = storage.upload_frame(
                buffer.tobytes(),
                filename = f"{job_id}_frame-{idx}.jpg"
            )

            result_detections.append(
                Detection(
                    timestamp = timestamp,
                    confidence = conf,
                    frame_key = frame_key
                )
            )

        result = JobResult(job_id = job_id, detections = result_detections)
        job_service.save_job_result(result)
        job_service.mark_job_completed(job_id)

    except Exception:
        logger.exception(
            "Inference failed",
            extra={"job_id": job_id}
        )
        job_service.mark_job_failed(job_id)