from enum import Enum

class EventType(Enum):
    EOS = 0
    SOS = 1
    ITEM_RCV = 2
    QUEUE_FSH = 10


class Event:

    def __init__(self, event_type, payload = None):
        self.event_type = event_type
        self.payload = payload
    
    def event_type(self):
        return self.event_type
    
    def payload(self):
        return payload
    
    @staticmethod
    def create_itemrcv(index, value, queue = None):
        return Event(EventType.ITEM_RCV, {"recipient_queue": queue, "index": index, "value": value})
    
    @staticmethod
    def create_sos(queue = None):
        return Event(EventType.SOS, {"recipient_queue": queue})

    @staticmethod
    def create_eos(queue = None):
        return Event(EventType.EOS, {"recipient_queue": queue})

    @staticmethod
    def create_finish(queue = None):
        return Event(EventType.QUEUE_FSH, {"recipient_queue": queue})