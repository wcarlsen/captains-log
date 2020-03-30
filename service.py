from os import getenv
import logging
from sys import stdout
import structlog
from src.kubernetes.event_steam import EventStream
from src.kubernetes.event import Event
from src.prometheus.server import PrometheusServer
from src.prometheus.metrics.event_counter import counter

logging.basicConfig(format="%(message)s", stream=stdout, level=logging.INFO)

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log = structlog.get_logger()

OFFSET: int = int(getenv("OFFSET", 5))

if __name__ == "__main__":
    log.info(f"Using offset {OFFSET} seconds to discard old events")

    ps: PrometheusServer = PrometheusServer()
    ps.serve()

    while True:
        es: EventStream = EventStream()

        for stream_event in es.start():
            event: Event = Event(stream_event)

            if event.is_old_event():
                continue

            log.info(
                f"Increment counter {event.reason} of {event.kind} in {event.namespace} for {event.name}"  # noqa: E501
            )
            counter.labels(event.kind, event.reason, event.namespace, event.name).inc()
