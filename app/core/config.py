import os

APP_ENV = os.getenv("APP_ENV", "local")

MODEL_URL = os.getenv("MODEL_URL", "https://github.com/aditya-4747/spitting-detection-system-streamlit-app/releases/download/v1.0-model/spitting_detection_model.pt")
MODEL_DIR = os.getenv("MODEL_DIR", "model")

DATA_DIR = os.getenv("DATA_DIR", "data")
VIDEO_DIR = os.path.join(DATA_DIR, "videos")
FRAME_DIR = os.path.join(DATA_DIR, "frames")

FRAME_INTERVAL = int(os.getenv("FRAME_INTERVAL", "30"))