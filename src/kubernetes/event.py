from os import getenv
from datetime import datetime, timezone
from structlog import get_logger

log = get_logger()

OFFSET: int = int(getenv("OFFSET", 5))


class Event(object):
    def __init__(self, event: dict) -> None:
        self.creation_timestamp: datetime = event["object"].metadata.creation_timestamp
        self.reason: str = event["object"].reason
        self.kind: str = event["object"].involved_object.kind
        self.namespace: str = event["object"].metadata.namespace
        self.name: str = event["object"].involved_object.name

    def is_old_event(self) -> bool:
        event_age: int = (datetime.now(timezone.utc) - self.creation_timestamp).seconds
        if event_age > OFFSET:
            log.debug(
                f"Skipping old event {self.reason} of {self.kind} in {self.namespace} for {self.name}",  # noqa: E501
                creation_timestamp=self.creation_timestamp.isoformat(),
                event_age=f"{event_age} seconds",
            )
            return True
        return False
