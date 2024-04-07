from plotconverter.plot_data_handler import PlotData
import matplotlib.pyplot as plt
import matplotlib as mpl


class MeanPlotter:

    def __init__(self):
        self.plot_data = PlotData(simulation_n="last")
        self.data = self.plot_data.get_plot_data(["stream_mean", "reservoir_mean"])


    def diff(self, x, y):
        difference = []
        zipped = zip(x, y)
        for t in zipped:
            if t[0] == "ND" or t[1] == "ND":
                difference.append("ND")
            else:
                difference.append(round(abs(t[0] - t[1]), 2))
        return difference
    
    def plot(self):
        
        offsets = self.data["offsets"]
        x = self.data["x"]

        stream_mean = self.data["stream_mean"]
        reservoir_mean = self.data["reservoir_mean"]
        diff_mean = self.diff(stream_mean, reservoir_mean)

        fig, ax = plt.subplots(2, 1)
        ax[0].set_xlabel("n")
        ax[1].set_xlabel("n")

        ax[0].set_ylabel("$\mu(n)$")
        ax[1].set_ylabel(r"$|\mu_s(n) - \mu_r(n)|$")

        ax[0].plot(x, stream_mean, label = "stream")
        ax[0].plot(x, reservoir_mean, label = "reservoir")
        ax[0].legend()

        ax[1].plot(x, diff_mean, color = "magenta", label = "s - r")

        for offset in offsets:
            ax[0].axvline(x = offset + 1, color = "red")

        plt.show()
