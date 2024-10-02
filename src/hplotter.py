import matplotlib.pyplot as plt
from plotconverter.histogram_plotter import HistogramPlotter
from statistics import mean
from config.config import get_condition


def main():
    simulation_n=[i for i in range(40, 50)]
    hp = HistogramPlotter(simulation_n=simulation_n)
    output = hp.plot()
    
    compressions = []
    distances = []
    eras = []
    sizes = []
    thresholds = []
    metrics = []
    for k in output:
        compressions.append(output[k]["compression"])
        distances.append(output[k]["histogram_distance"])
        eras.append(output[k]["number_of_eras"])
        sizes.append(output[k]["buffer_size"])
        thresholds.append(output[k]["threshold"])
        metrics.append(output[k]["metric"])

    anchor = output[simulation_n[0]]

    if all(map(lambda e: e == anchor["buffer_size"], sizes)) and all(map(lambda e: e == anchor["threshold"], thresholds)):
        print("/ =======================RESULTS======================== \\")
        print("Total simulations: " + str(len(simulation_n)))
        print("CV threshold: " + str(anchor["threshold"]))
        print("Reservoir size: " + str(anchor["buffer_size"]))
        print("Average number of eras: " + str(round(mean(eras), 3)))
        print("Average compression: " + str(round(mean(compressions), 3)))
        print("Average distance: " + str(round(mean(distances), 3)))
        print("Average metric: " + str(round(mean(metrics), 3)))
    else:
        print("Simulations discrepancies")

    


if __name__ == "__main__":
    main()