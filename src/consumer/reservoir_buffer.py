

class ReservoirBuffer:


    def __init__(self, size):
        self.size = size
        self.buffer = []

        # statistics
        self.mean = 0.0

    def consume(self, event):
        self.buffer.append(event.payload["value"])
        print(f"ReservoirBuffer consuming {event.event_type} with payload {event.payload}")


    def register_era_handler(self, era_handler):
        self.era_handler = era_handler