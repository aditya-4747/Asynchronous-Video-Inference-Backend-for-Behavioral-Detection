import os
import requests
import logging

from app.core.config import MODEL_URL, MODEL_DIR

MODEL_PATH = os.path.join(MODEL_DIR, "spitting-detection-model.pt")
logger = logging.getLogger(__name__)


def ensure_model_present() -> str:
    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(MODEL_PATH):
        logger.info("Model artifact found at /%s/spitting-detection-model.pt; skipping remote download", MODEL_DIR, extra={"path": MODEL_PATH})
        return MODEL_PATH

    logger.info("Model not found locally. Downloading...", extra={"URL": MODEL_URL})

    try:
        r = requests.get(MODEL_URL, stream=True, timeout=60)
        r.raise_for_status()

        with open(MODEL_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        logger.info("Model downloaded successfully", extra={"path": MODEL_PATH})
        return MODEL_PATH
    
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
            extra={"path": MODEL_PATH}
        )
        raise