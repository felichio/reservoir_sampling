from enum import Enum

class EventType(Enum):
    EOS = 0
    ITEM_RCV = 1


class Event:

    def __init__(self, event_type, payload = None):
        self.event_type = event_type
        self.payload = payload
    
    def event_type(self):
        return self.event_type
    
    def payload(self):
        return payload
    
    @staticmethod
    def create_itemrcv(index, value):
        return Event(EventType.ITEM_RCV, {"index": index, "value": value})
        
    @staticmethod
    def create_eos():
        return Event(EventType.EOS)