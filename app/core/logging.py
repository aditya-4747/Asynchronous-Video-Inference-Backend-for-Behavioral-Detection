import logging
import sys

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | job_id=%(job_id)s | %(message)s"
)

class SafeFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "job_id"):
            record.job_id = "-"
        return super().format(record)

def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(SafeFormatter(LOG_FORMAT))

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Remove existing handlers (important with Uvicorn)
    root.handlers.clear()

    root.addHandler(handler)