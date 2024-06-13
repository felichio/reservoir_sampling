import csv
import math
from plotconverter.plot_data_handler import PlotData


def convert_to_stddev(values):
    stddev = []
    for value in values:
        stddev.append(round(math.sqrt(value), 2))
    return stddev

def main():
    plot_data = PlotData("all", 1, "last")

    labels = ["stream_data", "stream_mean", "reservoir_mean", "stream_variance", "reservoir_variance"]


    csv_data = {}
    plot_data = plot_data.get_plot_data(labels)
    csv_data["x"] = plot_data["x"]
    for label in labels:
        csv_data[label] = plot_data[label]
    

    csv_data["stream_stddev"] = convert_to_stddev(csv_data["stream_variance"])
    csv_data["reservoir_stddev"] = convert_to_stddev(csv_data["reservoir_variance"])
    labels.append("stream_stddev")
    labels.append("reservoir_stddev")
    
    
    
    sample = len(csv_data["stream_data"])
    for key in csv_data:
        if len(csv_data[key]) != sample:
            raise Exception("invalid conversion")
    
    with open("cusum.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["n", "val", "stream_mean (w1)", "reservoir_mean (w2)", "stream_stddev (d1)", "reservoir_stddev (d2)", "w1 - w2", "max(d1,d2)"])
        for i in range(sample):
            n = csv_data["x"][i]
            value = csv_data["stream_data"][i]
            w1 = csv_data["stream_mean"][i]
            w2 = csv_data["reservoir_mean"][i]
            d1 = csv_data["stream_stddev"][i]
            d2 = csv_data["reservoir_stddev"][i]
            diff_w1_w2 = round(w1 - w2, 2)
            max_d1_d2 = max(d1, d2)
            writer.writerow([n, value, w1, w2, d1, d2, diff_w1_w2, max_d1_d2])
    
    


if __name__ == "__main__":
    main()