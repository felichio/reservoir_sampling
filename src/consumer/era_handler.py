from event.event import EventType
from config.config import get_output_folder
from config.config import get_condition
from config.config import settings
import os
import copy
import json

class EraHandler:

    class Era:

        def __init__(self, index_offset):
            self.stream_data = []
            self.reservoir_snapshots = []
            
            # stats
            self.index_offset = index_offset
            self.stream_mean_snapshots = []
            self.reservoir_mean_snapshots = []
            self.stream_variance_snapshots = []
            self.reservoir_variance_snapshots = []
            self.stream_coefficientvar_snapshots = []
            self.reservoir_coefficientvar_snapshots = []
        
        def fill_dict(self, output, field_name, values):
            temp = {}
            for i, item in enumerate(values):
                temp[i + 1] = item
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
            output["index_offset"] = self.index_offset
            self.fill_dict(output, "stream_data", self.stream_data)
            self.fill_dict(output, "reservoir", self.reservoir_snapshots)
            self.fill_dict(output, "stream_mean", self.stream_mean_snapshots)
            self.fill_dict(output, "reservoir_mean", self.reservoir_mean_snapshots)
            self.fill_dict(output, "stream_variance", self.stream_variance_snapshots)
            self.fill_dict(output, "reservoir_variance", self.reservoir_variance_snapshots)
            self.fill_dict(output, "stream_coefficientvar", self.stream_coefficientvar_snapshots)
            self.fill_dict(output, "reservoir_coefficientvar", self.reservoir_coefficientvar_snapshots)
            return output
        

    class Cusum:
        def __init__(self, properties):
            self.P = 0
            self.N = 0
            self.t = 0
            self.s_pos = 0
            self.s_neg = 0
            self.target_value = properties["target_value"]
            self.above_threshold = properties["above_threshold"]
            self.below_threshold = properties["below_threshold"]
            self.above_tolerance = properties["above_tolerance"]
            self.below_tolerance = properties["below_tolerance"]

        def calculate(self, x):
            print("---- Calculating CUSUM -----")
            self.P = max(0, x - (self.target_value + self.above_tolerance) + self.P)
            self.N = min(0, x - (self.target_value - self.below_tolerance) + self.N)
            print("P: " + str(self.P))
            print("N: " + str(self.N))
            print("x: " + str(x))
            if (self.P > self.above_threshold):
                self.s_pos += 1

            if (self.N < -self.below_threshold):
                self.s_neg += 1
            
            self.t += 1

    def __init__(self, stream_buffer, reservoir_buffer):
        self.stream_buffer = stream_buffer
        self.reservoir_buffer = reservoir_buffer
        self.eras = []
        
        self.eras.append(EraHandler.Era(0))
        self.condition = get_condition()


        # Create CUSUM instance in case of the the active condition says so
        if self.condition["active_condition"] == "cusum":
            self.cusum = EraHandler.Cusum(self.condition["properties"])


    def write_to_output(self):
        output_path = os.path.join(os.path.dirname(__file__), "..", "..", "output")
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_path = os.path.join(output_path, f"{str(get_output_folder())}")
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        output = {}
        output["reservoir_size"] = settings["reservoir_size"]
        output["active_condition"] = settings["active_condition"]
        output["conditions"] = settings["conditions"][settings["active_condition"]]
        for i, item in enumerate(self.eras):
            output[f"era_{i + 1}"] = item.to_json()
        
        with open(os.path.join(output_path, "eras.json"), "w", encoding = "utf-8") as f:
            json.dump(output, f, indent = 2)
    #counter = 0
    def is_era_completed(self, index_offset):
        
        # This check is triggered by every insertion happening inside the reservoir buffer.
        # complete_era
        # create a new era

        print("---- Reservoir stats ----")
        print("Reservoir: ", self.reservoir_buffer.buffer)        
        print("mean: ", self.reservoir_buffer.mean)
        print("variance: ", self.reservoir_buffer.variance)
        print("coefficient_var: ", self.reservoir_buffer.coefficientvar)

        if self.run_condition():
            self.complete_era()
            self.eras.append(EraHandler.Era(index_offset))
            return True
    
    def run_condition(self):
        

        if self.condition["active_condition"] == "cv_threshold":
            if self.stream_buffer.coefficientvar[0] != "ND" and self.reservoir_buffer.coefficientvar[0] != "ND" and self.stream_buffer.coefficientvar[0] != 0:
                print("CONDITION: |(cvs - cvr) / cvs| = " + str(abs((self.stream_buffer.coefficientvar[0] - self.reservoir_buffer.coefficientvar[0]) / self.stream_buffer.coefficientvar[0] )))
                if abs((self.stream_buffer.coefficientvar[0] - self.reservoir_buffer.coefficientvar[0]) / self.stream_buffer.coefficientvar[0] ) > self.condition["properties"]["threshold"]:
                    print("----CHANGING ERA----")
                    return True

        elif self.condition["active_condition"] == "cusum":
            x = self.stream_buffer.mean[0] - self.reservoir_buffer.mean[0]
            self.cusum.calculate(x)
            
            if self.cusum.s_pos > 0 or self.cusum.s_neg > 0:
                print("----CHANGING ERA----")
                return True
        return False


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
        era.stream_coefficientvar_snapshots = copy.deepcopy(self.stream_buffer.coefficientvar_snapshots)

        # Take the reservoir stats
        era.reservoir_mean_snapshots = copy.deepcopy(self.reservoir_buffer.mean_snapshots)
        era.reservoir_variance_snapshots = copy.deepcopy(self.reservoir_buffer.variance_snapshots)
        era.reservoir_coefficientvar_snapshots = copy.deepcopy(self.reservoir_buffer.coefficientvar_snapshots)

        # reset stream_buffer and reservoir_buffer states
        self.stream_buffer.clear_state()
        self.reservoir_buffer.clear_state()

        # create a new CUSUM instance to clear the previous state
        if self.condition["active_condition"] == "cusum":
            self.cusum = EraHandler.Cusum(self.condition["properties"])
    
    def consume(self, event):
        if event.event_type == EventType.EOS:
            print(f"EraHandler consuming {event.event_type} with payload {event.payload}")
            self.complete_era()
            self.write_to_output()
    

