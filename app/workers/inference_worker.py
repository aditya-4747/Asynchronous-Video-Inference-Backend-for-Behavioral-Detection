import cv2
import logging

from app.services import job_service
from app.core.database import SessionLocal
from app.models.frame import Frame
from app.models.detection import Detection
from app.services.job_service import storage
from app.services.model_loader import ensure_model_present
from app.services.inference_service import YoloInferenceService
from app.core.config import FRAME_INTERVAL

MODEL_PATH = ensure_model_present()
inference_service = YoloInferenceService(MODEL_PATH)
logger = logging.getLogger(__name__)


def process_job(job_id: str):
    logger.info("Worker started job processing", extra={"job_id": job_id})
    db = SessionLocal()

    try:
        job_service.mark_job_processing(job_id)

        job = job_service.get_job(job_id)
        video_path = storage.get_access_url(job.video_key)
        
        detections = inference_service.run(video_path, FRAME_INTERVAL)
        logger.info(
            "Inference completed", 
            extra={"job_id": job_id, "detections": len(detections)}
        )

        for idx, (timestamp, frame, spitting_instances) in enumerate(detections, start=1):
            success, buffer = cv2.imencode(".jpg", frame)
            if not success:
                continue

            frame_key = storage.upload_frame(
                buffer.tobytes(),
                job_id,
                filename = f"frame-{idx}.jpg"
            )

            frame = Frame(
                job_id=job_id,
                frame_key=frame_key,
                timestamp=timestamp
            )

            db.add(frame)
            db.flush()
            frame_id = frame.id

            for instance in spitting_instances:
                x1, y1, x2, y2 = instance["box"]

                detection = Detection(
                    frame_id=frame_id,
                    conf=instance["conf"],
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2
                )

                db.add(detection)

        db.commit()        
        job_service.mark_job_completed(job_id)

    except Exception:
        logger.exception(
            "Inference failed",
            extra={"job_id": job_id}
        )
        job_service.mark_job_failed(job_id)

    finally:
        db.close()