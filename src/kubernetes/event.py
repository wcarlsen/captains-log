from datetime import datetime, timezone
from structlog import get_logger

log = get_logger()

class Event(object):
    def __init__(self, event: dict) -> None:
        self.creation_timestamp: datetime = event["object"].metadata.creation_timestamp
        self.reason: str = event["object"].reason
        self.kind: str = event["object"].involved_object.kind
        self.namespace: str = event["object"].metadata.namespace
        self.name: str = event["object"].metadata.name

    def is_old_event(self) -> bool:
        event_age: int = (datetime.now(timezone.utc) - self.creation_timestamp).seconds
        if event_age > 5:
            log.info(f"Skipping old event", creation_timestamp=self.creation_timestamp, event_age=f"{event_age} seconds")
            return True
        return False

