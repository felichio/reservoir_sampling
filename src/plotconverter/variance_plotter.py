from plotconverter.plot_data_handler import PlotData
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

class VariancePlotter:

    def __init__(self, era_n = "all", dimension_n = 1, simulation_n = "last"):
        self.plot_data = PlotData(era_n, dimension_n, simulation_n)
        self.data = self.plot_data.get_plot_data(["stream_variance", "reservoir_variance"])


    def diff(self, x, y):
        difference = []
        zipped = zip(x, y)
        for t in zipped:
            difference.append(round(abs(t[0] - t[1]), 2))
        return difference
    
    def plot(self, range = None):
        
        offsets = self.data["offsets"]
        x = self.data["x"]

        stream_variance = self.data["stream_variance"]
        reservoir_variance = self.data["reservoir_variance"]

        if self.plot_data.era_n == "all" and range:
            low = min(range) - 1
            if len(range) > 1:
                high = max(range)
            else:
                high = None
        else:
            low = 0
            high = None

        # split eras for plotting (add nan to the beginning of every skipped era)
        if len(offsets) > 1:
            kindex = -1
            for i, offset in enumerate(offsets[:-1]):
                next_offset = offsets[i + 1]
                kindex += offset[1]
                
                if (offset[0] + offset[1]) < next_offset[0]:
                    kindex += 1
                    x.insert(kindex, np.nan)
                    stream_variance.insert(kindex, np.nan)
                    reservoir_variance.insert(kindex, np.nan)


        diff_variance = self.diff(stream_variance, reservoir_variance)

        fig, ax = plt.subplots(2, 1)
        ax[0].set_xlabel("n")
        ax[1].set_xlabel("n")

        ax[0].set_ylabel("$\sigma^2(n)$")
        ax[1].set_ylabel(r"$|\sigma^2_s(n) - \sigma^2_r(n)|$")

        ax[0].plot(x[low:high], stream_variance[low:high], label = "stream")
        ax[0].plot(x[low:high], reservoir_variance[low:high], label = "reservoir")
        ax[0].legend()

        ax[1].plot(x[low:high], diff_variance[low:high], color = "magenta", label = "s - r")

        ax[0].axhline(y = 0, linestyle = "dashed", color = "black")
        ax[1].axhline(y = 0, linestyle = "dashed", color = "black")
        
        for offset, era_label in zip(offsets, self.plot_data.era_labels):
            if (offset[0] + 1) in x[low:high]:
                ax[0].axvline(x = offset[0] + 1, color = "red", linestyle = "dotted")
                ax[0].text(x = offset[0] + 1, y = 0, s = era_label, rotation = 90, verticalalignment = "bottom")
                ax[1].axvline(x = offset[0] + 1, color = "red", linestyle = "dotted")
                ax[1].text(x = offset[0] + 1, y = 0, s = era_label, rotation = 90, verticalalignment = "bottom")
                
                ax[0].set_xticks(np.append(ax[0].get_xticks(), offset[0] + 1))
                ax[1].set_xticks(np.append(ax[0].get_xticks(), offset[0] + 1))

        plt.show()
