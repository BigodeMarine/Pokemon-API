import json
import logging
from datetime import datetime, UTC

"""
Formatter responsável por transformar os logs em JSON.
"""
class JsonFormatter(logging.Formatter):

    def format(self, record):

        log = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, "method"):
            log["method"] = record.method

        if hasattr(record, "path"):
            log["path"] = record.path

        if hasattr(record, "status"):
            log["status"] = record.status

        if hasattr(record, "duration_ms"):
            log["duration_ms"] = round(
                record.duration_ms,
                2,)
        if hasattr(record, "exception"):
            log["exception"] = record.exception


        return json.dumps(
            log,
            ensure_ascii=False,
        )