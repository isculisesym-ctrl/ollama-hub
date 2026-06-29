"""Request logging middleware — stores recent API requests in memory"""

import time
from collections import deque
from dataclasses import dataclass, field, asdict
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

MAX_LOG_ENTRIES = 500


@dataclass
class LogEntry:
    timestamp: str
    method: str
    path: str
    status_code: int
    duration_ms: float
    client_ip: str


_log_buffer: deque[LogEntry] = deque(maxlen=MAX_LOG_ENTRIES)


def get_logs(limit: int = 50, method: str | None = None, path_prefix: str | None = None) -> list[dict]:
    entries = list(_log_buffer)
    entries.reverse()
    if method:
        entries = [e for e in entries if e.method == method.upper()]
    if path_prefix:
        entries = [e for e in entries if e.path.startswith(path_prefix)]
    return [asdict(e) for e in entries[:limit]]


def get_log_stats() -> dict:
    entries = list(_log_buffer)
    if not entries:
        return {"total_requests": 0, "methods": {}, "status_codes": {}, "avg_duration_ms": 0}

    methods: dict[str, int] = {}
    status_codes: dict[int, int] = {}
    total_duration = 0.0

    for e in entries:
        methods[e.method] = methods.get(e.method, 0) + 1
        status_codes[e.status_code] = status_codes.get(e.status_code, 0) + 1
        total_duration += e.duration_ms

    return {
        "total_requests": len(entries),
        "methods": methods,
        "status_codes": {str(k): v for k, v in sorted(status_codes.items())},
        "avg_duration_ms": round(total_duration / len(entries), 2),
    }


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start) * 1000

        if request.url.path.startswith("/api/"):
            _log_buffer.append(LogEntry(
                timestamp=datetime.utcnow().isoformat() + "Z",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=round(duration, 2),
                client_ip=request.client.host if request.client else "unknown",
            ))

        return response
