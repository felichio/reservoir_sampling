import os
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
from config.config import settings
from plotconverter.plot_converter import PlotConverter
from plotconverter.plot_converter import PlotType
from plotconverter.mean_plotter import MeanPlotter
from plotconverter.variance_plotter import VariancePlotter
from plotconverter.coefficientvar_plotter import CoefficientVarPlotter


def main():
    
    
    mp = CoefficientVarPlotter(era_n = "all", simulation_n = "last", dimension_n = 1)
    mp.plot()


    



if __name__ == "__main__":
    main()

