from app.core.config import STORAGE_BACKEND
from app.storage.local import LocalStorageService
from app.storage.s3 import S3StorageService

def get_storage_service():
    if STORAGE_BACKEND == "s3":
        return S3StorageService
    
    return LocalStorageService