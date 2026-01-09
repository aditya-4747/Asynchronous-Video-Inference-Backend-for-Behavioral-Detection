import logging

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "job_id=%(job_id)s | %(message)s"
)

class SafeFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "job_id"):
            record.job_id = ""
        return super().format(record)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT
)

for handler in logging.root.handlers:
    handler.setFormatter(SafeFormatter(LOG_FORMAT))