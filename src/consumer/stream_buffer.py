


class StreamBuffer:

    def __init__(self):
        self.buffer = []



    def consume(self, event):
        self.buffer.append(event.payload["value"])
        print(f"StreamBuffer consuming {event.event_type} with payload {event.payload}")
        