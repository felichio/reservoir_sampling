import matplotlib.pyplot as plt
from plotconverter.histogram_plotter import HistogramPlotter


def main():
    hp = HistogramPlotter(simulation_n="last")
    hp.plot()
    


if __name__ == "__main__":
    main()