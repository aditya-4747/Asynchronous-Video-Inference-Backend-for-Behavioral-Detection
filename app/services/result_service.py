import cv2
import os
import shutil
import logging
import uuid
from typing import Optional

from app.models.result import JobResult
from app.core.config import TEMP_DIR

logger = logging.getLogger(__name__)

_RESULTS: dict[str, JobResult] = {}


def save_job_result(result: JobResult) -> None:
    _RESULTS[result.job_id] = result


def get_job_result(job_id: str) -> Optional[JobResult]:
    return _RESULTS.get(job_id)


def generate_preview(job_id: str) -> str:
    result = _RESULTS.get(job_id)

    # Unique ID per preview request to prevent temp-folder collisions between concurrent downloads
    request_id = uuid.uuid4().hex

    output_dir = os.path.join(TEMP_DIR, f"{job_id}_previews_{request_id}")
    os.makedirs(output_dir, exist_ok=True)

    idx = 1
    for det in result.detections:
        image = cv2.imread(det.frame_key)

        for item in det.instances:
            x1, y1, x2, y2 = item.box

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                color=(255, 0, 0),
                thickness=2
            )

            label = f"Spitting {item.conf:.2f}"
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
    with open(json_path, "w") as f:
        f.write(result.model_dump_json())

    # Download the results (zip file)
    zip_name = os.path.join(TEMP_DIR, f"{job_id}_results")
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