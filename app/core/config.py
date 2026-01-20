from dotenv import load_dotenv
import os

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "local")
STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")

MODEL_URL = os.getenv("MODEL_URL", "https://github.com/aditya-4747/spitting-detection-system-streamlit-app/releases/download/v1.0-model/spitting_detection_model.pt")

# Local development variables
DATA_DIR = os.getenv("DATA_DIR", "data")
VIDEO_DIR = os.path.join(DATA_DIR, "videos")
FRAME_DIR = os.path.join(DATA_DIR, "frames")

TEMP_DIR = os.path.join(DATA_DIR, "temp")

FRAME_INTERVAL = int(os.getenv("FRAME_INTERVAL", "30"))

DATABASE_URL = os.getenv("DATABASE_URL")

# AWS configurations
AWS_REGION = os.getenv("AWS_REGION")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "spitting-detection-storage")