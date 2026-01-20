import tempfile
import os
from typing import BinaryIO
from app.storage.base import StorageService
from app.infrastructure.s3_client import upload_file, generate_presigned_url

class S3StorageService(StorageService):
    def upload_video(file: BinaryIO, filename: str) -> str:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file)
            temp_path = tmp.name

        key = f"uploads/{filename}"
        upload_file(temp_path, key)

        return key
    
    def get_access_url(key: str) -> str:
        return generate_presigned_url(key)
    
    def upload_frame(image_bytes: bytes, job_id: str, filename: str) -> str:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(image_bytes)
            temp_path = tmp.name

        key = f"frames/{job_id}/{filename}"
        upload_file(temp_path, key)

        return key