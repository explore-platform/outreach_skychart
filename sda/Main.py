
"""
Author: Lian Greijn
Creation Date: 04-10-2023
Latest Update: 04-10-2023

Function: Test possibilities of visualizing Interstellar Dust to the night sky view of an observer on Earth. 
"""
#General Imports
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib as mpl
import pandas as pd
mplstyle.use('fast')        #Make matplotlib a bit faster
import time

#Import functions from other files [See readme for overview] 
from integrated_dust_data import getintegratedcoordinates, to_altaz
from constellation_data import query_constellations
from solarsystem import get_solarsystem
from plotter import create_plot

#Astropy imports
import astropy.units as u
from astropy.coordinates import EarthLocation 
from astropy.time import Time



#User inputs
obs_loc = EarthLocation(lat=50.85*u.deg, lon=4.3517*u.deg)
utcoffset = 0*u.hour  # CEST time
obs_time = Time('2023-11-6 23:50:00') - utcoffset

#Calling all the functions to generate the dustdata 
table = getintegratedcoordinates()
dust_data = to_altaz(table, obs_loc, obs_time)

#Getting solar system data
solarsystem = get_solarsystem(obs_loc, obs_time)
constellations, constellationinfo, consname = query_constellations(obs_loc, obs_time)


#Plot using Plotly
fig = create_plot(dust_data, solarsystem, constellations, constellationinfo, consname, obs_time)
plt.show()





