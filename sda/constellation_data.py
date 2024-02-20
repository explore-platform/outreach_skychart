# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 17:18:09 2023

@author: lgreijn
"""
import numpy as np
from astroquery.simbad import Simbad
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_body, get_icrs_coordinates
from astropy.time import Time
import pandas as pd
#from astropy.table import Table

'''
obs_loc = EarthLocation(lat=50.85*u.deg, lon=4.3517*u.deg)
utcoffset = 1*u.hour  # CEST time
obs_time = Time('2023-11-6 4:35:00') - utcoffset 
'''

filename = './data/ConstellationLines.dat' #file containing HIP names of the stars in each constellation

def query_constellations(obs_loc, obs_time):
    #Prepare data tables
    names_column = []
    starnum_column =[]
    stars = []
    
    #Read data file and extract info of each constellation
    with open(filename) as file:
        content = list(file)
        for idx, line in enumerate(content):
          element = line.split()
          
          #Save to corresponding columns
          names_column.append(element[0])
          starnum_column.append(int(element[1]))
          stars.append(element[2:])

    #Initialize loop
    splitting_indices = np.zeros((len(starnum_column), 2))
    previous = 0
    
    #Create table with info where splits should be made
    for idx, item in enumerate(starnum_column):
        new = previous+int(item)
        splitting_indices[idx] = [previous, new]
        previous = new 
    #Convert to array with integers so indices can be called correctly
    splitting_indices = np.array(splitting_indices, dtype = 'int')
    
    #Prepare data for loop
    querytable = np.zeros((sum(starnum_column) ,3))
    i = 0 
    brightnessfile = './data/star_data.txt'
    
    #initialize tables
    magV = []
    coordinate_list = []
    
    #Read star brightness values and coordinates
    with open(brightnessfile) as file:
        content = list(file)
        for idx, line in enumerate(content):
          element = line.split(';')
          magV.append(element[-1])
      
          #Split coordinate data 
          coordinates_raw = element[-2]
          coordinates_raw = coordinates_raw.split()
          coordinate_ra = float(coordinates_raw[0])
          coordinate_dec = float(coordinates_raw[1])
          
          #Store coordinates
          coordinates = [coordinate_ra, coordinate_dec]
          coordinate_list.append(coordinates)
          
    #Query each stars coordinate and matching brightness      
    for row in stars:
       for element in row:
           newquery= SkyCoord(coordinate_list[i][0], coordinate_list[i][1], frame = 'icrs', unit = (u.deg, u.deg)).transform_to(AltAz(obstime=obs_time,location=obs_loc))
           
           #Set brightnesslevel for the body
           brightness = magV[i]
           
           #Filters for data errors 
           if brightness == '     ~   \n':
                brightness = 4.5 #set an average value if no data is available
                   
           final_brightness = 6.5 - float(brightness)
           if float(final_brightness) <= 0:
               final_brightness = 0.3
           
           #Add coordinates and final brightness into table
           querytable[i] = [newquery.az.deg, newquery.alt.deg, final_brightness] 
           i = i+1

                
    return querytable, splitting_indices, names_column

