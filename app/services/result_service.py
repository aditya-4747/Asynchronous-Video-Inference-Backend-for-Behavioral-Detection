import cv2
import os
import shutil
from typing import Optional

from app.models.result import JobResult

_RESULTS: dict[str, JobResult] = {}


def save_job_result(result: JobResult) -> None:
    _RESULTS[result.job_id] = result


def get_job_result(job_id: str) -> Optional[JobResult]:
    return _RESULTS.get(job_id)


def generate_preview(job_id: str) -> str:
    result = _RESULTS.get(job_id)

    output_dir = f"data/temp/{job_id}_previews"
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
                color=(0, 0, 255),
                thickness=2
            )

            label = f"Spitting conf={item.conf:.2f}"
            cv2.putText(
                image,
                label,
                (x1, y1-10),
                cv2.FONT_HERSHEY_COMPLEX,
                0.6,
                (0, 0, 255),
                2
            )

        frame_path = f"{output_dir}/preview-{idx}.jpg"
        cv2.imwrite(frame_path, image)
        idx += 1


    # Dump the detections in JSON file
    json_path = f"{output_dir}/detections.json"
    with open(json_path, "w") as f:
        f.write(result.model_dump_json())

    # Download the results (zip file)
    zip_name = f"data/temp/{job_id}_results"
    archive_path = shutil.make_archive(zip_name, 'zip', output_dir)

    return archive_path