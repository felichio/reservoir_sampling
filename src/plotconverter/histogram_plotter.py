import json
import os
from config.config import settings
from config.config import get_condition
import matplotlib.pyplot as plt
import numpy as np

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
                era_labels.remove("active_condition")
                era_labels.remove("conditions")
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
            output_simulation_data["active_condition"] = simulation_data["active_condition"]
            output_simulation_data["conditions"] = simulation_data["conditions"]

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

            # append number of eras
            output_simulation_data["number_of_eras"] = len(era_labels)

            output_simulation_data["stream_data"] = stream_data
            output_simulation_data["reservoir_data"] = reservoir_data
            self.output_data[simulation_n] = output_simulation_data
            
        
        

    
    def plot(self):
        number_of_bins = settings["bins"]
        output = {}
        for simulation_n in self.output_data:
            stream_data = [x for item in self.output_data[simulation_n]["stream_data"] for x in item]
            reservoir_data = [x for item in self.output_data[simulation_n]["reservoir_data"] for x in item]
            
            min_stream = min(stream_data)
            max_stream = max(stream_data)
            min_reservoir = min(reservoir_data)
            max_reservoir = max(reservoir_data)

            fig, ax = plt.subplots(2, 2)

            L = max_stream - min_stream

            s = ax[0, 0].hist(stream_data, number_of_bins, color='yellow', edgecolor='black', )
            r = ax[1, 0].hist(reservoir_data, number_of_bins, color='blue', edgecolor='black', range=(min_stream, max_stream))

            sd = ax[0, 1].hist(stream_data, number_of_bins, color='yellow', edgecolor='black', density=True)
            rd = ax[1, 1].hist(reservoir_data, number_of_bins, color='blue', edgecolor='black', range=(min_stream, max_stream), density=True)
            #print(s)
            #print(r)
            

            ax[0, 0].ticklabel_format(style='plain')
            ax[1, 0].ticklabel_format(style='plain')
            ax[0, 1].ticklabel_format(style='plain')
            ax[1, 1].ticklabel_format(style='plain')

            ax[0, 0].legend(("stream",))
            ax[0, 1].legend(("stream",))
            ax[1, 0].legend(("buffer",))
            ax[1, 1].legend(("buffer",))

            ax[0, 0].set_ylabel(r"$\sum_{j=1}^{N} χ(x_j, I_i)$")
            ax[1, 0].set_ylabel(r"$\sum_{j=1}^{M} χ(y_j, I_i)$")
            ax[0, 1].set_ylabel(r"$\frac{K}{NL}\sum_{j=1}^{N} χ(x_j, I_i)$")
            ax[1, 1].set_ylabel(r"$\frac{K}{ML}\sum_{j=1}^{M} χ(y_j, I_i)$")
            ax[0, 0].set_xlabel(r"$x_j$")
            ax[1, 0].set_xlabel(r"$y_j$")
            ax[0, 1].set_xlabel(r"$x_j$")
            ax[1, 1].set_xlabel(r"$y_j$")


            threshold = self.output_data[simulation_n]["conditions"]["threshold"]
            Eras = self.output_data[simulation_n]["number_of_eras"]
            r = self.output_data[simulation_n]["reservoir_size"]
            K = number_of_bins
            N = len(stream_data)
            M = len(reservoir_data)
            Lr = max_reservoir - min_reservoir
            compression = round((1 - M / N), 4)
            print("------------------------------")
            print("Simulation no. " + str(simulation_n))
            print("No. eras = " + str(Eras))
            print("r size = " + str(r))
            print("threshold: " + str(threshold))

            print("K = " + str(K))
            print("N = " + str(N))
            print("M = " + str(M))
            print("L = Ls = " + str(int(L)))
            print("Lr = " + str(int(Lr)))
            print("compression = " + str(round(compression * 100, 2)) + "%")

            
            histogram_distance = sum(map(lambda e: abs(e[0] - e[1]) * L / K, zip(sd[0], rd[0])))
            # histogram_distance_2 = sum(map(lambda e: abs((e[0] / N) - (e[1] / M)), zip(s[0], r[0])))
            print("Histogram Distance = " + str(histogram_distance))
            # print(histogram_distance_2)
            metric = round(compression / histogram_distance, 3)

            print("Metric = " + str(metric))

            output[simulation_n] = {
                "simulation_number": simulation_n,
                "number_of_eras": Eras,
                "buffer_size": r,
                "threshold": threshold,
                "K": K,
                "N": N,
                "M": M,
                "L": L,
                "Lr": Lr,
                "compression": compression,
                "histogram_distance": histogram_distance.item(),
                "metric": metric
            }
            
            
            plt.show()
        return output


        
