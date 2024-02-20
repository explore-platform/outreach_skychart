# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 14:57:17 2023

@author: lgreijn
"""
import numpy as np
from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_body
from astropy.table import QTable
from astropy.time import Time
import astropy.units as u

def get_solarsystem(obs_loc, obs_time):
    #Import skycoord of each body in solar system and transform to alt, az coordinates
    sun_loc = get_body(body = 'sun', 
                        location = obs_loc, 
                        time = obs_time
                        ).transform_to(AltAz(obstime=obs_time,location=obs_loc))
    
    moon_loc = get_body(body = 'moon', 
                        location = obs_loc, 
                        time = obs_time
                        ).transform_to(AltAz(obstime=obs_time,location=obs_loc))
    
    mercury_loc = get_body(body = 'mercury', 
                        location = obs_loc, 
                        time = obs_time
                        ).transform_to(AltAz(obstime=obs_time,location=obs_loc))
    
    venus_loc = get_body(body = 'Venus', 
                        location = obs_loc, 
                        time = obs_time
                        ).transform_to(AltAz(obstime=obs_time,location=obs_loc))
    
    mars_loc = get_body(body = 'mars', 
                        location = obs_loc, 
                        time = obs_time
                        ).transform_to(AltAz(obstime=obs_time,location=obs_loc))
    
    jupiter_loc = get_body(body = 'jupiter', 
                        location = obs_loc, 
                        time = obs_time
                        ).transform_to(AltAz(obstime=obs_time,location=obs_loc))

    saturn_loc = get_body(body = 'saturn', 
                        location = obs_loc, 
                        time = obs_time
                        ).transform_to(AltAz(obstime=obs_time,location=obs_loc))

    uranus_loc = get_body(body = 'uranus', 
                        location = obs_loc, 
                        time = obs_time
                        ).transform_to(AltAz(obstime=obs_time,location=obs_loc))
    
    neptune_loc = get_body(body = 'neptune', 
                        location = obs_loc, 
                        time = obs_time
                        ).transform_to(AltAz(obstime=obs_time,location=obs_loc))
    
    #Create columns for final table containing name, position, color and markersize
    body_list = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    
    #Save planets azimuth coordinates
    az_list = [sun_loc.az,
               moon_loc.az,
               mercury_loc.az, 
               venus_loc.az, 
               mars_loc.az, 
               jupiter_loc.az, 
               saturn_loc.az,
               uranus_loc.az,
               neptune_loc.az]
    
    #Save planets altitude coordinates
    alt_list = [sun_loc.alt,
                moon_loc.alt,
                mercury_loc.alt,
                venus_loc.alt,
                mars_loc.alt,
                jupiter_loc.alt,
                saturn_loc.alt,
                uranus_loc.alt,
                neptune_loc.alt]
    
    #Define color of each planet in the plot
    color = ['#F0F935', 
             '#BDBDBD',
             '#CAC7BE',
             '#F4EECD',
             '#B90000',
             '#D1A716',
             '#9F7F0E',
             '#0FBEE9',
             '#0668C3']
    
    #Size in the plot
    size = [15, 5,  3, 7, 6, 12, 10, 8, 8]
    
    #Create final table
    solarsystem_table = QTable([body_list, az_list, alt_list, color, size], #Finalize table
                               names=('body','az','alt','color','size'))
    return solarsystem_table

