# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 15:07:28 2023

@author: lgreijn
"""


import h5py
import numpy as np
import astropy.units as u
from astropy.table import QTable
from astropy.coordinates import AltAz, SkyCoord

def getintegratedcoordinates():
    filepath = './data/grid_lbdext_0.5deg_5pc.h5'
    f = h5py.File(filepath, 'r')        #open the datacube file
    
    #Extract relevant data from h5 file and transfer to array
    data_l = np.array(f['l'])
    data_b = np.array(f['b'])
    data_e = np.array(f['e'])
    
    #Integrate the extinction over the distance 
    summed_extinction = np.sum(data_e, axis = 2) 
    summed_e = summed_extinction.flatten() #Flatten the data so all coordinates can be matched to corresponding point
    summed_e_log = np.log10(summed_e)
    
    #Create meshgrid of the l & b arrays
    xx, yy= np.meshgrid(data_b, data_l) 
    
    #Flattening the meshgrid so that each coordinatepoint is vertically stacked with columns [b,l]
    coord_list = np.vstack((xx.flatten(), yy.flatten())).T
   
    #Making a table from with the coordinates and data 
    dust_table = QTable(data = [coord_list[:,1]*u.rad, coord_list[:,0]*u.rad, summed_e_log], names=('l', 'b', 'data'))
    
    return dust_table


def to_altaz(data_table, obs_loc, obs_time):
    #Extract coordinates from table
    sc_l = data_table['l'] 
    sc_b = data_table['b']
    
    #Make the coordinates them Skycoordinate objects for easy transformation
    sc = SkyCoord(l = sc_l, b = sc_b, frame ='galactic')
    
    #Transform them to altitude azimuth coordinates
    sc_transform_altaz = sc.transform_to(AltAz(obstime=obs_time, location=obs_loc))
    sc_altaz = sc_transform_altaz.to_table()
    sc_altaz['data'] = data_table['data'] #re-add the data.
    
    return sc_altaz
