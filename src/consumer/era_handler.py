from event.event import EventType
from config.config import get_output_folder
import os
import copy
import json

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
        
        def fill_dict(self, output, field_name, values):
            temp = {}
            for i, item in enumerate(values):
                temp[i] = item
            output[field_name] = temp

        def to_json(self):
            output = {}
            # stream_data = {}
            # for i, item in enumerate(self.stream_data):
            #     stream_data[i] = item
            # output["stream_data"] = stream_data
            # reservoir = {}
            # for i, item in enumerate(self.reservoir_snapshots):
            #     reservoir[i] = item
            # output["reservoir"] = reservoir
            self.fill_dict(output, "stream_data", self.stream_data)
            self.fill_dict(output, "reservoir", self.reservoir_snapshots)
            self.fill_dict(output, "stream_mean", self.stream_mean_snapshots)
            self.fill_dict(output, "reservoir_mean", self.reservoir_mean_snapshots)
            self.fill_dict(output, "stream_variance", self.stream_variance_snapshots)
            self.fill_dict(output, "reservoir_variance", self.reservoir_variance_snapshots)
            
            return output

    def __init__(self, stream_buffer, reservoir_buffer):
        self.stream_buffer = stream_buffer
        self.reservoir_buffer = reservoir_buffer
        self.eras = []
        
        self.eras.append(EraHandler.Era())


    def write_to_output(self):
        output_path = os.path.join(os.path.dirname(__file__), "..", "output")
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_path = os.path.join(output_path, f"{str(get_output_folder())}")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        output = {}
        for i, item in enumerate(self.eras):
            output[f"era_{i + 1}"] = item.to_json()
        
        with open(os.path.join(output_path, "eras.json"), "w", encoding = "utf-8") as f:
            json.dump(output, f, indent = 2)
    
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
        self.stream_buffer.clear_state()
        self.reservoir_buffer.clear_state()
    
    def consume(self, event):
        if event.event_type == EventType.EOS:
            print(f"EraHandler consuming {event.event_type} with payload {event.payload}")
            self.complete_era()
            self.write_to_output()
    

