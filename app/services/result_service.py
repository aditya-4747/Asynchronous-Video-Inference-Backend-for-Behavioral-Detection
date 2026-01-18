import cv2
import os
import shutil
import logging
import uuid
import json
from collections import defaultdict

from app.core.config import TEMP_DIR
from app.core.database import SessionLocal
from app.models.frame import Frame
from app.models.detection import Detection

logger = logging.getLogger(__name__)

def format_job_result(rows) -> dict:
    grouped = defaultdict(lambda: {
        "timestamp": None,
        "frame_key": None,
        "instances": []
    })

    for frame, det in rows:
        key = frame.id
        
        if grouped[key]["timestamp"] is None:
            grouped[key]["timestamp"] = frame.timestamp
            grouped[key]["frame_key"] = frame.frame_key
        
        grouped[key]["instances"].append({
            "conf": det.conf,
            "box": [
                int(det.x1),
                int(det.y1),
                int(det.x2),
                int(det.y2)
            ]
        })

    return list(grouped.values())


def get_job_result(job_id: str):
    db = SessionLocal()
    try:
        rows = (
            db.query(Frame, Detection)
            .join(Detection, Detection.frame_id == Frame.id)
            .filter(Frame.job_id == job_id)
            .order_by(Frame.timestamp)
            .all()
        )

        if not rows:
            return {}
        
        detections = format_job_result(rows)
        return {
            "job_id": job_id,
            "detections": detections
        }

    finally:
        db.close()


def generate_preview(job_id: str) -> str:
    result = get_job_result(job_id=job_id)

    if result == {}:
        return "", ""

    # Unique ID per preview request to prevent temp-folder collisions between concurrent downloads
    request_id = uuid.uuid4().hex

    output_dir = os.path.join(TEMP_DIR, f"{job_id}_previews_{request_id}")
    os.makedirs(output_dir, exist_ok=True)

    idx = 1
    for det in result['detections']:
        image = cv2.imread(det['frame_key'])

        for item in det['instances']:
            x1, y1, x2, y2 = item['box']

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                color=(255, 0, 0),
                thickness=2
            )

            label = f"Spitting {item['conf']:.2f}"
            cv2.putText(
                image,
                label,
                (x1, y1-10),
                cv2.FONT_HERSHEY_COMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

        frame_path = f"{output_dir}/preview-{idx}.jpg"
        cv2.imwrite(frame_path, image)
        idx += 1


    # Dump the detections in JSON file
    json_path = os.path.join(output_dir, "detections.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    # Download the results (zip file)
    zip_name = os.path.join(TEMP_DIR, f"{job_id}_results_{request_id}")
    archive_path = shutil.make_archive(zip_name, 'zip', output_dir)

    return archive_path, output_dir


def cleanup_temp_files(zip_path: str, temp_folder: str):
    try:
        if os.path.exists(zip_path):
            os.remove(zip_path)
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
        
    except Exception:
        logger.warning("Failed to clean temporary preview files")