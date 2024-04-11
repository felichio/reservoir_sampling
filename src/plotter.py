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
    
    
    mp = CoefficientVarPlotter(era_n = "all", simulation_n = 2, dimension_n = 1)
    mp.plot([1, 16409])


    



if __name__ == "__main__":
    main()

