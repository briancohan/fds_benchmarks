# FDS Benchmarks

As part of the SFPE Advanced Fire Dynamics Simulator (FDS) course, students were asked to run a number of models to see the effect of mesh resolution and MP Threads on simulation time.
This repo provides an exploration of the results.

The original data can be found in this [Google sheet](https://docs.google.com/spreadsheets/d/1RgDj0EAtFC8vVzdeue0ylMd3vPxi-Oxj43dIZpr__Sk/).
The data is also retained in the `data` directory of this repository.
The FDS files used are provided in the `data` directory as well.

The `benchmark` directory contains modules to help keep the appearance of the [Jupyter Notebook](https://jupyter.org/) clean.

Click [here](https://nbviewer.jupyter.org/github/briancohan/fds_benchmarks/blob/main/Explore.ipynb) to explore the interactive charts.
Click [here](https://mybinder.org/v2/gh/briancohan/fds_benchmarks/HEAD?filepath=Explore.ipynb) if you would like to play with the data yourself (this may take a few moments to start).

# Preview of results

Below is a very brief overview of what is laid out in the analysis. Please checkout the [full analysis](https://nbviewer.jupyter.org/github/briancohan/fds_benchmarks/blob/main/Explore.ipynb) for more information including interactive charts.

## Summary of Computational Power

Most students appeared to be working on normal workstations, but a few were using higher end machines.

![computer_power](/images/computer_power.png)

## Grid Resolution Effect on Heat Detector Activation

The grid resolution had a significant effect on run time, but a minimal effect on heat detector activation time.

![grid_wall_time](/images/grid_wall_time.png)

![grid_heat_detector_time](/images/grid_heat_detector_time.png)

## OpenMP Thread

The number of threads used had a diminishing return once the number of threads per core was exceeded.

![omp_wall_time](/images/omp_wall_time.png)
