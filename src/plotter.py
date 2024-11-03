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
import argparse


def main():
    
    parser = argparse.ArgumentParser(prog="Plotter for Reservoir Sampling Simulation")
    parser.add_argument("-e", "--eras", default=-1, type=int, nargs="*" )
    parser.add_argument("-s", "--simulation", default=-1, type=int)
    parser.add_argument("-d", "--dimension", default=1)
    parser.add_argument("-r", "--range", default=[], nargs=2, type=int)
    parser.add_argument("-p", "--plot", choices=["mean", "variance", "coefficient_variance"], default="coefficient_variance")

    args = parser.parse_args()
    if args.eras == -1:
        args.eras = "all"
    if args.simulation == -1:
        args.simulation = "last"
    
    

    if args.plot == "mean":
        p = MeanPlotter(era_n=args.eras, simulation_n=args.simulation, dimension_n=args.dimension)
    elif args.plot == "variance":
        p = VariancePlotter(era_n=args.eras, simulation_n=args.simulation, dimension_n=args.dimension)
    elif args.plot == "coefficient_variance":
        p = CoefficientVarPlotter(era_n=args.eras, simulation_n=args.simulation, dimension_n=args.dimension)
    p.plot(args.range)


    



if __name__ == "__main__":
    main()

