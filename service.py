from sys import stdout
from os import getenv
from datetime import datetime, timezone
from prometheus_client import start_http_server, Counter
from kubernetes import client, config, watch
import structlog

# Logging
def timestamper(_, __, event_dict):
    event_dict["timestamp"] = datetime.now(timezone.utc).isoformat()
    return event_dict


structlog.configure(
    processors=[
        timestamper,
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)
logger = structlog.get_logger()

# Kubernetes
config.load_kube_config(config_file="~/.kube/config_hellman")
v1 = client.CoreV1Api()
w = watch.Watch()

# Prometheus
PORT = int(getenv("PORT", "8080"))

c = Counter(
    "deployments_total", "Total number of deployments", ["reason", "namespace", "name"]
)


# Service
if __name__ == "__main__":
    logger.info(f"Start service at port={PORT}")

    # Start up the server to expose the metrics.
    start_http_server(port=PORT)

    logger.info("Consuming events")
    for event in w.stream(v1.list_event_for_all_namespaces):
        logger.info(f"Event recieved of type {event['object'].reason}", creationtime=event["object"].metadata.creation_timestamp)

        # Probably old event and or unrelated
        if (
            datetime.now(timezone.utc) - event["object"].metadata.creation_timestamp
        ).seconds < 10:
            logger.info("Incrementing counter metric")
            c.labels(
                event["object"].reason,
                event["object"].metadata.namespace,
                event["object"].metadata.name,
            ).inc()
