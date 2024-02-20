# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 14:00:29 2023

@author: lgreijn
"""

# -*- coding: utf-8 -*-
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
import pandas as pd
mplstyle.use('fast')        #Make matplotlib a bit faster


#Import functions from other files [See readme for overview] 
#from dust_data_interpreter import get_data, data_properties, Dust, to_altaz
from integrated_dust_data import getintegratedcoordinates, to_altaz
from constellation_data import query_constellations
from solarsystem import get_solarsystem
from plotter import create_plot
'''
from PlotlyPlotter import create_plotly

#Bokeh Imports
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser'
'''
#Astopy imports
import astropy.units as u
from astropy.coordinates import EarthLocation 
from astropy.time import Time


#Extinction data input eventueel uit UI laten halen
data_location = './data/' #Folder in which datacube is stored
data_name = 'explore_cube_density_values_050pc_v1.h5' #actual datafile name
file = data_location + data_name #Creating path to datafile 


#User inputs
obs_loc = EarthLocation(lat=30*u.deg, lon=40*u.deg)
utcoffset = 2*u.hour  # CEST time
obs_time = Time('2023-10-17 5:3:00') - utcoffset 
treshold = 10**-4*u.mag

table = getintegratedcoordinates()


hourrange = list(range(0,24))
minuterange = np.arange(0, 60, 5).tolist()
i = 0
for hour in hourrange:
    for minute in minuterange:
        plotname = './timelapseplots/nightsky' + str(i) + '.png'
        date = '2023-11-06'
        time_string = str(date + ' ' + str(hour)+ ':' + str(minute)+ ':00')
        obs_loc = EarthLocation(lat=50.85*u.deg, lon=4.3517*u.deg)
        utcoffset = 1*u.hour  # CEST time
        obs_time = Time(time_string) - utcoffset 
        print('starting with ', plotname)


        #Getting solar system data
        dust_data = to_altaz(table, obs_loc, obs_time)
        solarsystem = get_solarsystem(obs_loc, obs_time)
        constellations, constellationinfo, consname = query_constellations(obs_loc, obs_time)

        #Plot using Plotly
        fig = create_plot(dust_data, solarsystem, constellations, constellationinfo, consname, obs_time)
        plt.savefig(plotname)
        i = i+1
        print('saved plot', plotname)
        plt.close()





