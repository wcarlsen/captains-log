from prometheus_client import Counter

NAME: str = "events_total"
DOCUMENTATION: str = "Total number of events"
LABELS: list = ["kind", "reason", "namespace", "name"]

counter: Counter = Counter(NAME, DOCUMENTATION, LABELS)