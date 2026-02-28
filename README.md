# Satellite-Data-Processing

The scripts here are used as tools to automate the processing of satellite data gathered in compliance with our high school subject: STEM Research 3. Our research is entitled:

> Evaluating the Trends of Remotely-Sensed Chlorophyll-A and Sea Surface Temperature and their Influence on Bali Sardinella (Sardinella lemuru) Landings in Zamboanga Del Norte.

The NC_Processing.py script automates the generation of images (PNG) of our pre-processed satellite data (NetCDF files). The pre-processed NetCDF files are already masked to our study region, so the file facilitates in plotting them to a graph complete with a colorbar of the variable, latitude and longitude markers, and city markers.

The GIF_maker.py script facilitates the creation of a GIF of all the processed satellite data to create an animation.

The DescriptiveStatistics.py gathers the descriptive statistics of all NetCDF files in the directory and organizes them in a CSV file for further analysis.

Note: This code was written in 2024, and I was kinda messy with my code back then.
