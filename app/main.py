from fastapi import FastAPI
import logging

from app.api.health import router as health_router
from app.api.jobs import router as jobs_router
from app.core.config import APP_ENV

app = FastAPI(title="Spitting Detection Backend")
logger = logging.getLogger(__name__)


app.include_router(health_router)
app.include_router(jobs_router)

logger.info("Application started", extra={ "env": APP_ENV })