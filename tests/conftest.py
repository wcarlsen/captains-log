import pytest
from src.prometheus.server import PrometheusServer

ps: PrometheusServer = PrometheusServer()


@pytest.fixture(scope="module")
def client() -> None:
    ps.serve()
