FROM python:3.11-slim

WORKDIR /app

# System dependencies required by OpenCV
RUN apt-get update \
    && apt-get install -y libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/


# Install CPU-only PyTorch explicitly
RUN pip install --no-cache-dir \
    torch==2.2.2+cpu \
    torchvision==0.17.2+cpu \
    torchaudio==2.2.2+cpu \
    --index-url https://download.pytorch.org/whl/cpu


# App dependencies 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY migrations/ migrations/
COPY app/ app/

# Model download
RUN mkdir model
RUN wget -O model/spitting-detection-model.pt https://github.com/aditya-4747/spitting-detection-system-streamlit-app/releases/download/v1.0-model/spitting_detection_model.pt

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]