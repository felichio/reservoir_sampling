

class Dummy:



    def consume(self, event):
        print(f"Consuming {event.event_type} with payload {event.payload}")