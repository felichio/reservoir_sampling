from event.event import EventType
from event.event import Event

class QueueFinish:

    def consume(self, event):
        if event.event_type == EventType.QUEUE_FSH:
            ceq = event.payload["recipient_queue"]
            ceq.finish()