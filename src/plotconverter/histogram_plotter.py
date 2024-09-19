import json
import os
from config.config import settings
import matplotlib.pyplot as plt

class HistogramPlotter:
    
    def __init__(self, era_n = "all", dimension_n = 1, simulation_n = "last"):
        self.era_n = era_n
        self.dimension_n = dimension_n
        self.simulation_n = simulation_n
        self.read_data()
        self.prepare_data()


    def read_data(self):
        if self.simulation_n == "last":
            last_output_folder = [settings["output_directory_number"] - 1]
        elif type(self.simulation_n) == list:
            last_output_folder = self.simulation_n

        self.simulations = {}
        filename = "eras.json"
        for k in last_output_folder:
            output_path = os.path.join(os.path.dirname(__file__), "..", "..", "output", str(k))
            with open(os.path.join(output_path, filename)) as f:
                eras = json.load(f)
                self.simulations[k] = eras
    

    def prepare_data(self):
        self.output_data = {}
        for simulation_n in self.simulations:
            if self.era_n == "all":
                era_labels = list(self.simulations[simulation_n].keys())
                era_labels.remove("reservoir_size")
            else:
                era_labels = []
                for era_n in sorted(self.era_n):
                    era_label = f"era_{era_n}"
                    if era_label in self.eras:
                        era_labels.append(era_label)
            
            simulation_data = self.simulations[simulation_n]
            output_simulation_data = {}

            # append reservoir_size
            output_simulation_data["reservoir_size"] = simulation_data["reservoir_size"]

            # append stream data
            stream_data = []
            reservoir_data = []
            for era_label in era_labels:
                stream_data_era = []
                
                for k in simulation_data[era_label]["stream_data"]:
                    item = simulation_data[era_label]["stream_data"][k]
                    stream_data_era.append(item[self.dimension_n - 1])
                stream_data.append(stream_data_era)

                reservoir_data_era = []
                reservoir_key_snapshots = simulation_data[era_label]["reservoir"].keys()
                

                for k in reversed(reservoir_key_snapshots):
                    
                    item = simulation_data[era_label]["reservoir"][k]
                    if item[0] == "-":
                        continue
                    else:
                        for inner_item in item:
                            reservoir_data_era.append(inner_item[self.dimension_n - 1])
                        break
                reservoir_data.append(reservoir_data_era)

            output_simulation_data["stream_data"] = stream_data
            output_simulation_data["reservoir_data"] = reservoir_data
            self.output_data[simulation_n] = output_simulation_data
        
        

    
    def plot(self):
        number_of_bins = settings["bins"]
        for simulation_n in self.output_data:
            stream_data = [x for item in self.output_data[simulation_n]["stream_data"] for x in item]
            reservoir_data = [x for item in self.output_data[simulation_n]["reservoir_data"] for x in item]

            min_stream = int(min(stream_data))
            max_stream = int(max(stream_data))
            


            plt.hist(stream_data, number_of_bins, color='yellow', edgecolor='black')
            plt.ticklabel_format(style='plain')
            plt.show()


        
