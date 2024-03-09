import threading
import queue
from event.event import EventType

class EventQueue:
    

    def __init__(self):
        self.queue = queue.Queue()
        self.event_listeners = {}
        for event_name in list(EventType):
            self.event_listeners[event_name] = []
        




    def dispatch(self, event):
        listeners = self.event_listeners[event.event_type]
        for listener in listeners:
            listener.consume(event)

    def subscribe(self, event_type, listener):
        self.event_listeners[event_type].append(listener)