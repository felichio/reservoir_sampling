import os
import json
from config.config import settings
import numpy as np


class PlotData:

    def __init__(self, era_n = "all", dimension_n = 1, simulation_n = "last"):
        self.era_n = era_n
        self.dimension_n = dimension_n
        self.simulation_n = simulation_n
        self.read_eras()
        

    def read_eras(self):
        last_output_folder = self.simulation_n
        if self.simulation_n == "last":
            last_output_folder = settings["output_directory_number"] - 1
        
        output_path = os.path.join(os.path.dirname(__file__), "..", "..", "output", str(last_output_folder))
        filename = "eras.json"

        with open(os.path.join(output_path, filename)) as f:
            eras = json.load(f)
            self.eras = eras
            

    def get_plot_data(self, stats_labels):
        if self.era_n == "all":
            era_labels = list(self.eras.keys())
        else:
            era_labels = []
            for era_n in sorted(self.era_n):
                era_label = f"era_{era_n}"
                if era_label in self.eras:
                    era_labels.append(era_label)
        print(era_labels)
        self.era_labels = era_labels
        x = []
        # [(offset, length)]
        offsets = []
        for era_label in era_labels:
            offset = self.eras[era_label]["index_offset"]
            x = x + [offset + int(i) for i in self.eras[era_label]["stream_data"]]
            offsets.append((offset, len(self.eras[era_label]["stream_data"])))
        
        data = {}
        data["offsets"] = offsets
        data["x"] = x
        for stat in stats_labels:
            data_y = []
            for era_label in era_labels:
                data_era_y = []
                for key in self.eras[era_label][stat]:
                    item = self.eras[era_label][stat][key]
                    if item[0] == "-":
                        data_era_y.append(data_era_y[-1])
                    elif item[0] == "ND":
                       data_era_y.append(np.nan)
                    else:
                        data_era_y.append(round(item[self.dimension_n - 1], 2))
                data_y += data_era_y
            data[stat] = data_y
        return data

        

