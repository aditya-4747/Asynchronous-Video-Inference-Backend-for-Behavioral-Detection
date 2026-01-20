import os
import shutil
from typing import BinaryIO

from app.storage.base import StorageService
from app.core.config import VIDEO_DIR, FRAME_DIR

class LocalStorageService(StorageService):
    def __init__(self):
        os.makedirs(VIDEO_DIR, exist_ok=True)
        os.makedirs(FRAME_DIR, exist_ok=True)

    def upload_video(self, file: BinaryIO, filename: str) -> str:
        key = filename
        path = os.path.join(VIDEO_DIR, key)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(file, buffer)

        return key
    
    def get_access_url(self, key: str) -> str:
        return os.path.join(VIDEO_DIR, key)
    
    def upload_frame(self, image_bytes: bytes, job_id: str, filename: str) -> str:
        frame_folder = os.path.join(FRAME_DIR, job_id)
        os.makedirs(frame_folder, exist_ok=True)

        path = os.path.join(frame_folder, filename)

        with open(path, "wb") as f:
            f.write(image_bytes)

        return path