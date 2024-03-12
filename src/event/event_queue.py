import threading
import queue
from event.event import EventType

class EventQueue:
    

    def __init__(self):
        self.queue = queue.Queue()
        self.event_listeners = {}
        for event_name in list(EventType):
            self.event_listeners[event_name] = []
        

    def enqueue(self, event):
        self.queue.put(event)


    def dispatch(self, event):
        listeners = self.event_listeners[event.event_type]
        for listener in listeners:
            listener.consume(event)

    def subscribe(self, event_type, listener):
        self.event_listeners[event_type].append(listener)

    
    def run(self):
        while True:
            print("blocked")
            ev = self.queue.get()
            print(f"dispatching {ev}")
            self.dispatch(ev)
            self.queue.task_done()

            # end condition
            if ev.event_type == EventType.EOS:
                break