

class EraHandler:

    class Era:

        def __init__(self):
            self.stream_buffer_data = []
            self.reservoir_buffer_data = []
            
            # stats
            self.stream_buffer_mean = ()
            self.reservoir_buffer_mean = ()
            self.stream_buffer_variance = ()
            self.reservoir_buffer_variance = ()


    def __init__(self, stream_buffer, reservoir_buffer):
        self.stream_buffer = stream_buffer
        self.reservoir_buffer = reservoir_buffer
        self.eras = []
        self.eras.append(EraHandler.Era())

    
    def is_era_completed(self):
        pass
        # This check is triggered by every insertion happening inside the reservoir buffer.

    def complete_era(self):
        print("completing era")
        era = self.eras[-1] # get the last era
        # Take the stream data. Make a copy
        era.stream_buffer_data = self.stream_buffer.buffer[:]
        # Take the reservoir buffer data. Make a copy
        era.reservoir_buffer_data = self.reservoir_buffer.buffer[:]

        # Stats
        # Take the stream stats
        era.stream_buffer_mean = tuple(self.stream_buffer.mean)
        era.stream_buffer_variance = tuple(self.stream_buffer.variance)

        # Take the reservoir stats
        era.reservoir_buffer_mean = tuple(self.reservoir_buffer.mean)
        era.reservoir_buffer_variance = tuple(self.reservoir_buffer.variance)
    
    def consume(self, event):
        print(f"EraHandler consuming {event.event_type} with payload {event.payload}")
        self.complete_era()