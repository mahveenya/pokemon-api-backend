import json
import logging
import time
from uuid import uuid4

from starlette.requests import Request
from starlette.responses import Response

from app.constants import REQUEST_ID_HEADER
from app.logging_config import tracking_id_var

logger = logging.getLogger("app.access")


def _capture_body(raw: bytes):
    """Return the body as a single string (exact bytes), or None when empty.

    Kept as a string on purpose: VictoriaLogs flattens nested JSON objects into
    separate `payload.<key>` fields, so a parsed dict would fragment. A string
    stays one copyable `payload` field.
    """
    if not raw:
        return None
    return raw.decode("utf-8", errors="replace")


async def access_log(request: Request, call_next):
    tracking_id = request.headers.get(REQUEST_ID_HEADER) or uuid4().hex
    token = tracking_id_var.set(tracking_id)
    request.state.tracking_id = tracking_id

    # Starlette's BaseHTTPMiddleware caches the body, so reading it here does not
    # starve the downstream endpoint.
    request_body = _capture_body(await request.body())

    method = request.method
    path = request.url.path
    received_extra = {
        "event": "request.received",
        "log_type": "access",
        "method": method,
        "path": path,
        "query": request.url.query,
        "client": request.client.host if request.client else None,
        "headers": json.dumps(dict(request.headers), ensure_ascii=False),
    }
    received_msg = f"Incoming request: {method} {path}"
    if request_body is not None:
        received_extra["payload"] = request_body
        received_msg += f" payload: {request_body}"
    logger.info(received_msg, extra=received_extra)

    start = time.perf_counter()
    try:
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.exception(
                f"Failed request: {method} {path} 500",
                extra={
                    "event": "request.completed",
                    "log_type": "access",
                    "method": method,
                    "path": path,
                    "status_code": 500,
                    "duration_ms": duration_ms,
                },
            )
            raise

        raw = b"".join([chunk async for chunk in response.body_iterator])
        response_body = _capture_body(raw)
        headers = dict(response.headers)
        headers.pop("content-length", None)
        response = Response(
            content=raw,
            status_code=response.status_code,
            headers=headers,
        )

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        route = request.scope.get("route")
        route_path = route.path if route else path
        route_name = getattr(route, "name", None)

        response.headers[REQUEST_ID_HEADER] = tracking_id
        completed_extra = {
            "event": "request.completed",
            "log_type": "access",
            "method": method,
            "path": path,
            "route": route_path,
            "route_name": route_name,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        }
        completed_msg = (
            f"Completed request: {method} {path} "
            f"{response.status_code} ({duration_ms}ms)"
        )
        if response_body is not None:
            completed_extra["payload"] = response_body
            completed_msg += f" payload: {response_body}"
        logger.info(completed_msg, extra=completed_extra)
        return response
    finally:
        tracking_id_var.reset(token)
