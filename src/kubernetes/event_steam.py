from os import getenv
from typing import Optional, Generator
from kubernetes import config
from kubernetes.watch import Watch
from kubernetes.client import CoreV1Api
from structlog import get_logger

log = get_logger()


class EventStream(object):
    def __init__(self) -> None:
        self.kube_config: Optional[str] = getenv("KUBECONFIG")
        self.__load_config()
        self.__core_v1_api: CoreV1Api = CoreV1Api()
        self.__watcher: Watch = Watch()

    def __load_config(self) -> None:
        if self.kube_config:
            log.info(
                "Loading Kubernetes configuration",
                configuration="outside-cluster",
                config_file=self.kube_config,
            )
            config.load_kube_config(config_file=self.kube_config)
        else:
            log.info("Loading Kubernetes configuration", configuration="inside-cluster")
            config.load_incluster_config()

    def start(self) -> Generator[dict, None, None]:
        log.info("Start steaming Kubernetes events from all namespaces")
        return self.__watcher.stream(
            self.__core_v1_api.list_event_for_all_namespaces
        )
