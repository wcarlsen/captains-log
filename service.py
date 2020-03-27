from os import getenv
import logging
from sys import stdout
import structlog
from prometheus_client import start_http_server
from src.kubernetes.event_steam import EventStream
from src.kubernetes.event import Event
from src.prometheus.event_counter import counter

logging.basicConfig(format="%(message)s", stream=stdout, level=logging.INFO)

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log = structlog.get_logger()

PORT = getenv("PORT", "8080")
OFFSET: int = int(getenv("OFFSET", 5))

if __name__ == "__main__":
    log.info(f"Using offset {OFFSET} seconds to discard old events")
    log.info(f"Star serving metrics on port {PORT}")
    start_http_server(int(PORT))

    while True:
        es: EventStream = EventStream()

        for stream_event in es.start():
            event: Event = Event(stream_event)

            if event.is_old_event():
                continue

            log.info(
                f"Increment counter {event.reason} of {event.kind} in {event.namespace} for {event.name}"
            )
            counter.labels(event.kind, event.reason, event.namespace, event.name).inc()
