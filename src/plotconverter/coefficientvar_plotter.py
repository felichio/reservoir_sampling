from plotconverter.plot_data_handler import PlotData
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


class CoefficientVarPlotter:

    def __init__(self, era_n = "all", dimension_n = 1, simulation_n = "last"):
        self.plot_data = PlotData(era_n, dimension_n, simulation_n)
        self.data = self.plot_data.get_plot_data(["stream_coefficientvar", "reservoir_coefficientvar"])


    def diff(self, x, y):
        difference = []
        zipped = zip(x, y)
        for t in zipped:
            difference.append(round(abs(t[0] - t[1]), 2))
        return difference
    
    def plot(self):
        
        offsets = self.data["offsets"]
        x = self.data["x"]

        stream_coefficientvar = self.data["stream_coefficientvar"]
        reservoir_coefficientvar = self.data["reservoir_coefficientvar"]

        # split eras for plotting (add nan to the beginning of every skipped era)
        if len(offsets) > 1:
            kindex = -1
            for i, offset in enumerate(offsets[:-1]):
                next_offset = offsets[i + 1]
                kindex += offset[1]
                
                if (offset[0] + offset[1]) < next_offset[0]:
                    kindex += 1
                    x.insert(kindex, np.nan)
                    stream_coefficientvar.insert(kindex, np.nan)
                    reservoir_coefficientvar.insert(kindex, np.nan)
        
        diff_coefficientvar = self.diff(stream_coefficientvar, reservoir_coefficientvar)

        fig, ax = plt.subplots(2, 1)
        ax[0].set_xlabel("n")
        ax[1].set_xlabel("n")

        ax[0].set_ylabel("$Cv(n)$")
        ax[1].set_ylabel(r"$|Cv_s(n) - Cv_r(n)|$")

        ax[0].plot(x, stream_coefficientvar, label = "stream")
        ax[0].plot(x, reservoir_coefficientvar, label = "reservoir")
        ax[0].legend()

        ax[1].plot(x, diff_coefficientvar, color = "magenta", label = "s - r")

        for offset in offsets:
            ax[0].axvline(x = offset[0] + 1, color = "red", linestyle = "dotted")
            ax[0].axhline(y = 0, linestyle = "dashed", color = "black")
            ax[1].axvline(x = offset[0] + 1, color = "red", linestyle = "dotted")

        plt.show()
