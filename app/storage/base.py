from abc import ABC, abstractmethod
from typing import BinaryIO

class StorageService(ABC):

    @abstractmethod
    def upload_video(self, file: BinaryIO, filename: str) -> str:
        pass

    def get_access_url(self, key: str) -> str:
        pass

    def upload_frame(self, image_bytes: bytes, filename: str) -> str:
        pass