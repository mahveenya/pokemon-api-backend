from contextvars import ContextVar
from datetime import UTC, datetime
import json
import logging
import re
import sys

from app.constants import SERVICE_NAME

tracking_id_var: ContextVar[str] = ContextVar("tracking_id", default="-")

# Fields that live on every LogRecord; anything else is treated as an `extra`.
_RESERVED = set(logging.makeLogRecord({}).__dict__.keys()) | {
    "message",
    "asctime",
    "tracking_id",
}


class TrackingIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.tracking_id = tracking_id_var.get()
        return True


# SQLAlchemy chatter to drop: parameter/metadata lines ([raw sql], [generated
# in ...], [cached ...]) and the dialect's connection-setup probes. Transaction
# markers (BEGIN/COMMIT/ROLLBACK) and real statements are kept.
_SQL_NOISE = re.compile(
    r"^\["
    r"|^select pg_catalog\.version"
    r"|^select current_schema"
    r"|^show ",
    re.IGNORECASE,
)


class SqlLogFilter(logging.Filter):
    """Drop SQLAlchemy noise, and relabel the surviving SQL from INFO (how
    SQLAlchemy emits it) to DEBUG, so SQL sits below the INFO-level API access
    logs and can be filtered separately (`level:DEBUG`)."""

    def filter(self, record: logging.LogRecord) -> bool:
        if record.name.startswith("sqlalchemy"):
            if _SQL_NOISE.match(record.getMessage()) is not None:
                return False
            record.levelno = logging.DEBUG
            record.levelname = "DEBUG"
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "service": SERVICE_NAME,
            "tracking_id": getattr(record, "tracking_id", "-"),
            "message": record.getMessage(),
        }

        for key, value in record.__dict__.items():
            if key not in _RESERVED and not key.startswith("_"):
                payload[key] = value

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    handler.addFilter(TrackingIdFilter())
    handler.addFilter(SqlLogFilter())

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.DEBUG)

    # The access logger owns its handler and does not propagate, so request
    # lines are always JSON regardless of how uvicorn configures the root.
    access = logging.getLogger("app.access")
    access.handlers = [handler]
    access.setLevel(logging.DEBUG)
    access.propagate = False

    # INFO logs statements + transaction markers (DEBUG additionally dumps every
    # result row). SqlLogFilter then strips the [param]/probe noise and relabels
    # the surviving SQL to DEBUG, so it sits below the INFO-level API logs.
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
