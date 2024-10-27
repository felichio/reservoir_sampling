# Reservoir Sampling
Simulation Program supporting findings described in diploma thesis

Written in Python 3.12

## Installation
Use the python venv module to create a virtual environment
```bash
python -m vevn vevn
source venv/bin/activate
```

Install the requirements
```bash
pip install -r requirements.txt
```

Place a csv file inside the input folder.

Adjust the config/config.json file accordingly.


## Execution
- main.py
```bash
python src/main.py
```
Executing main.py will actually run the simulation. The input will be parsed, and the specified dimensions will be consumed by the
reservoir sampler. Epochs will be created based on the active condition. The results of the run will be stored inside the output folder
structure, on the subfolder with the largest number (starting point is 0). The structure of the results will be a json file, and will contain
all the useful data for each Epoch. Statistical indexes per time $t$, input stream element, as well as the reservoir buffer state for each $t$.

- plotter.py
```bash
python src/plotter.py
```
Executing plotter.py will plot the specified statistical measurements for the input stream as well as the reservoir buffers. Available metrics are
mean, variance, and Coefficient of Variation. Eras, dimensions, as well as ranges of $t$ can be adjusted for better visualization of the plots. 

- hplotter.py
```bash
python src/hplotter.py
```
Executing hplotter.py will plot the histogram plots of a simulation. Input stream, and the scattered through Epochs buffer elements define the two (2) samples.
The number of subintervals $K$ (bins) can be specified in the config.json. file. The output also prints information for the histogram creation as well as the distance, compression
and efficiency metrics.