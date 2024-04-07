import os
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
from config.config import settings
from plotconverter.plot_converter import PlotConverter
from plotconverter.plot_converter import PlotType
from plotconverter.mean_plotter import MeanPlotter

LAST_OUTPUT_FOLDER = settings["output_directory_number"] - 1
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "output", str(LAST_OUTPUT_FOLDER))
FILENAME = "eras.json"


def read_eras():
    with open(os.path.join(OUTPUT_PATH, FILENAME)) as f:
        eras = json.load(f)
    return eras

def main():
    
    # print(OUTPUT_PATH)
    # eras = read_eras()
    # pc = PlotConverter(eras, 1, 1)
    # pc.convert(PlotType.COEFFICIENT_VAR)
    # pc.plot([1, 3000])
    mp = MeanPlotter()
    mp.plot()


    



if __name__ == "__main__":
    main()

