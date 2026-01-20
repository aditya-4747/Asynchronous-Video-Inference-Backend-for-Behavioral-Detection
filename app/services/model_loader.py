import os
import requests
import logging
from app.core.config import MODEL_URL

logger = logging.getLogger(__name__)

def ensure_model_present() -> str:
    model_path = "model/spitting-detection-model.pt"
    os.makedirs("model", exist_ok=True)

    if os.path.exists(model_path):
        logger.info("Model artifact found at /model/spitting-detection-model.pt; skipping remote download")
        return model_path

    logger.info("Model not found locally. Downloading...")

    try:
        r = requests.get(MODEL_URL, stream=True, timeout=60)
        r.raise_for_status()

        with open(model_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        logger.info("Model downloaded successfully", extra={"path": model_path})
        return model_path
    
    except requests.RequestException:
        logger.error(
            "Model download failed (Network/HTTP)",
            exc_info=True,
            extra={"url": MODEL_URL}
        )
        raise

    except OSError:
        logger.error(
            "Model download failed (Filesystem error)",
            exc_info=True,
            extra={"path": model_path}
        )
        raise