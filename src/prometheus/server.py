from os import getenv
from structlog import get_logger
from prometheus_client import start_http_server

log = get_logger()


class PrometheusServer(object):
    def __init__(self) -> None:
        self.port = int(getenv("PORT", "8080"))

    def serve(self) -> None:
        log.info(f"Star serving metrics on port {self.port}")
        start_http_server(port=self.port)
