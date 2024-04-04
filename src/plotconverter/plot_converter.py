import matplotlib.pyplot as plt
import matplotlib as mpl
from enum import Enum

class PlotType(Enum):
    MEAN = 0
    VARIANCE = 1
    COEFFICIENT_VAR = 2


class PlotConverter:

    



    def __init__(self, eras, era_n, dimension_n):
        self.eras = eras
        self.era_n = era_n
        self.dimension_n = dimension_n
    

    def convert(self, plot_type):
        if plot_type == PlotType.MEAN:
            stream = self.eras[f"era_{self.era_n}"]["stream_mean"]
            reservoir = self.eras[f"era_{self.era_n}"]["reservoir_mean"]
        elif plot_type == PlotType.VARIANCE:
            stream = self.eras[f"era_{self.era_n}"]["stream_variance"]
            reservoir = self.eras[f"era_{self.era_n}"]["reservoir_variance"]
        elif plot_type == PlotType.COEFFICIENT_VAR:
            stream = self.eras[f"era_{self.era_n}"]["stream_coefficientvar"]
            reservoir = self.eras[f"era_{self.era_n}"]["reservoir_coefficientvar"]

        # x axis values
        x = [int(x) for x in stream.keys()]
        
        # y axis values for stream
        stream_y = self.get_y_values(stream)
        # y axis values for reservoir
        reservoir_y = self.get_y_values(reservoir)
        # y axis values for abs difference between two above
        diff_y = self.get_diff_values(stream_y, reservoir_y)

        self.stream_data = (x, stream_y)
        self.reservoir_data = (x, reservoir_y)
        self.diff_data = (x, diff_y)

            
    def get_diff_values(self, a, b):
        diff = []
        zipped = zip(a, b)
        for t in zipped:
            if t[0] == "ND" or t[1] == "ND":
                diff.append("ND")
            else:
                diff.append(round(abs(t[0] - t[1]), 2))
        return diff


    def get_y_values(self, store):
        y_values = []
        for key in store:
            item = store[key]
            if item[0] == "-":
                y_values.append(y_values[-1])
            elif item[0] == "ND":
                y_values.append("ND")
            else:
                y_values.append(round(item[self.dimension_n - 1], 2))
        return y_values


    def plot(self, range = None):
        if range == None:
            low = 1
            high = None
        else:
            low = min(range)
            high = max(range)


        fig, ax = plt.subplots(1, 2)
        
        ax[0].plot(self.stream_data[0][(low - 1):high], self.stream_data[1][(low - 1):high], label = "stream")
        ax[0].plot(self.reservoir_data[0][(low - 1):high], self.reservoir_data[1][(low - 1):high], label = "reservoir")
        # ax[0].set_xticks(self.stream_data[0][(low - 1):high])
        ax[0].legend()
        print(self.reservoir_data[1][(low - 1):high])
        ax[1].plot(self.diff_data[0][(low - 1):high], self.diff_data[1][(low - 1):high])
        plt.show()