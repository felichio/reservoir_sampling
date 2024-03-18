from event.event import EventType
from event.event import Event

class StreamItemGenerator:

    def __init__(self, stream_iterator):
        self.iter = stream_iterator

    def consume(self, event):
        if event.event_type == EventType.SOS:
            ceq = event.payload["recipient_queue"]
            for i, item in enumerate(self.iter):
                ceq.enqueue(Event.create_itemrcv(i + 1, item))
        elif event.event_type == EventType.EOS:
            ceq = event.payload["recipient_queue"]
            ceq.enqueue(Event.create_eos())

