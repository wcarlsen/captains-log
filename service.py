from os import getenv
import structlog
from prometheus_client import start_http_server
from src.kubernetes.event_steam import EventStream
from src.kubernetes.event import Event
from src.prometheus.event_counter import counter

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(),
        structlog.processors.JSONRenderer(),
    ]
)

log = structlog.get_logger()

PORT = getenv("PORT", "8080")

if __name__ == "__main__":
    log.info(f"Star serving metrics on port {PORT}")
    start_http_server(int(PORT))

    while True:
        es: EventStream = EventStream()

        for stream_event in es.start():
            event: Event = Event(stream_event)

            if event.is_old_event():
                continue

            log.info(f"Increasing counter for {event.kind} {event.reason} in {event.namespace} {event.name}")
            counter.labels(event.kind, event.reason, event.namespace, event.name).inc()

