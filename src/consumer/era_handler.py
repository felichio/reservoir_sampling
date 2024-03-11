from event.event import EventType
import copy

class EraHandler:

    class Era:

        def __init__(self):
            self.stream_data = []
            self.reservoir_snapshots = []
            
            # stats
            self.stream_mean_snapshots = []
            self.reservoir_mean_snapshots = []
            self.stream_variance_snapshots = []
            self.reservoir_variance_snapshots = []


    def __init__(self, stream_buffer, reservoir_buffer):
        self.stream_buffer = stream_buffer
        self.reservoir_buffer = reservoir_buffer
        self.eras = []
        self.eras.append(EraHandler.Era())

    
    def is_era_completed(self):
        pass
        # This check is triggered by every insertion happening inside the reservoir buffer.
        # complete_era
        # create a new era

    def complete_era(self):
        print("completing era")
        era = self.eras[-1] # get the last era
        # Take the stream data. Make a copy
        era.stream_data = self.stream_buffer.buffer[:]
        # Take the reservoir buffer data. Make a copy
        era.reservoir_snapshots = copy.deepcopy(self.reservoir_buffer.buffer_snapshots)

        # Stats
        # Take the stream stats
        era.stream_mean_snapshots = copy.deepcopy(self.stream_buffer.mean_snapshots)
        era.stream_variance_snapshots = copy.deepcopy(self.stream_buffer.variance_snapshots)

        # Take the reservoir stats
        era.reservoir_mean_snapshots = copy.deepcopy(self.reservoir_buffer.mean_snapshots)
        era.reservoir_variance_snapshots = copy.deepcopy(self.reservoir_buffer.variance_snapshots)


        # reset stream_buffer and reservoir_buffer states
        # todo
    
    def consume(self, event):
        if event.event_type == EventType.EOS:
            print(f"EraHandler consuming {event.event_type} with payload {event.payload}")
            self.complete_era()