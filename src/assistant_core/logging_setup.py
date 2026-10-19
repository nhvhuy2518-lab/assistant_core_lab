import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    """
    Format log records as structured JSON strings.
    Guarantees no sensitive data (like API keys) is printed.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        for key in ("intent", "latency_ms", "session", "degraded"):
            if hasattr(record, key):
                log_data[key] = getattr(record, key)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure root/package logger to output JSON formatted logs to stderr.
    """
    logger = logging.getLogger("assistant_core")
    logger.setLevel(log_level.upper())

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)  
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger