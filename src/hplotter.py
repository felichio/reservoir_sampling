import matplotlib.pyplot as plt
from plotconverter.histogram_plotter import HistogramPlotter


def main():
    hp = HistogramPlotter(simulation_n=[8, 9])
    hp.read_data()
    


if __name__ == "__main__":
    main()