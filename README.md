# ROCKE3D_CloudDynamics-Habitability
ROCKE3D is a planetary GCM designed by NASA GISS and is commonly used to explore the atmospheric and oceanic dynamics of exoplanets. My project uses model output from ROCKE-3D to explore the relationship between cloud dynamics and surface temperature, with surface temperature serving as metric of habitability.

All the functions I created are in master_ROCKE3D.py with examples of their use scattered around in .ipynb files. Model simulations are in all of the A** and O** files.

AIJ - averaged over all layers
AIJK - 40 layers
AIJL - 40 pressure levels
AJL - zonal, with 40 pressure levels
OIJL - ocean simulations

ROCKE-3D model simulations are available online at:
https://portal.nccs.nasa.gov/GISS_modelE/ROCKE-3D/publication-supplements/Climates_of_Warm_Earth_like_Planets_I/

From the paper:
Way, M. J., Del Genio, A. D., Aleinov, I., Clune, T. L., Kelley, M., &amp; Kiang, N. Y. (2018). Climates of warm Earth-like planets. I. 3D Model Simulations. The Astrophysical Journal Supplement Series, 239(2), 24. https://doi.org/10.3847/1538-4365/aae9e1 
