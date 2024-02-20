# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:02:57 2023

@author: lgreijn
"""

#Importing required libraries
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import matplotlib as mpl
from matplotlib import cm, ticker

mplstyle.use('fast')        #Make matplotlib a bit faster

def create_plot(dust_data, solarsystem, constellations, constellationinfo, consname, obstime):
    
    #Plot initialization
    plt.figure(figsize=(9, 9)) #intialize plot and set size
    ax = plt.subplot(111, projection='polar') #make a circular plot
    ax.set_rlim(bottom=90, top=0) #Flipping the r axis to match astronomical definitions
    ax.tick_params(axis='x', which = 'major', pad = 15)
    
    
    #Reading the observation time
    obstime = obstime.value.split('.')
    plotdate_time = obstime[0].split()

    #Setting labels for axes and plot
    plt.title('Night sky above Brussels on ' + plotdate_time[0] + ' at ' + plotdate_time[1])
    ax.set_xlabel('Azimuth [deg]')
    plt.text(0.73, 0.98, "Altitude [deg]", transform=ax.transAxes, color = 'silver') #create artificial axis label 
    
    # Customize the plot, adding background color etc.
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_facecolor('#041A40') 
    ax.tick_params(axis='y', colors='silver') #change color of r ticks to make plot more readable
    
    #Setting labels for azimuth values
    theta_angles = (0, 45, 90, 135, 180, 225, 270, 315)
    theta_labels = ('0° N', '45° NE', '90° E','135° SE', '180° S','225° SW','270° W', '315° NW')
    plt.thetagrids(angles=theta_angles, labels=theta_labels)
    
    #Extract coordinates and magnitudes
    azimuths =dust_data['az'].rad.flatten() #Should be radians due to matplotlib polar plot logic
    altitudes = dust_data['alt'].deg.flatten()
    magnitudes = dust_data['data'].value.flatten()
    
    #Create normalization for plot coloring (can be changed in case of outliers)
    cmin = np.percentile(magnitudes, 0)
    cmax = np.percentile(magnitudes, 100)
    cmap = mpl.cm.inferno
    norm = mpl.colors.Normalize(vmin = cmin, vmax = cmax)
    
    #Plot the extinction values
    plt.scatter(azimuths,
                altitudes, 
                s = magnitudes*0.5,
                c = magnitudes,
                cmap = 'inferno',
                )
    
    #Add colorbar to plot
    plt.colorbar(mpl.cm.ScalarMappable(norm = norm, cmap = cmap),
                 ax=ax,
                 pad = 0.1,
                 fraction = 0.04,
                 orientation = 'vertical',
                 label = 'Extinction level [$log_{10}$ mag]')
    
    #Plotting the solar system data for each body
    for idx, body in enumerate(solarsystem['body']):
        plt.scatter(np.radians(solarsystem['az'][idx]), 
                    solarsystem['alt'][idx], 
                    color=str(solarsystem['color'][idx]), 
                    s = solarsystem['size'][idx])
        #also plot name of the body a bit to the side of the marker, if the body is within plot limits
        if solarsystem['alt'][idx].value >= 0:
            plt.text(np.radians(solarsystem['az'][idx].value)+0.05, 
                        solarsystem['alt'][idx].value,
                        body,
                        color = str(solarsystem['color'][idx]))
        
    #Plotting the constellations
    previousname = ''
    for idx, line in enumerate(constellationinfo):
        if all(i <= 0 for i in constellations[line[0]:line[1], 1]) == False:
            #Done with both scatter and plot because matplotlib does not support varying markersizes in just plot
            plt.scatter(np.radians(constellations[line[0]:line[1], 0]),
                        constellations[line[0]:line[1], 1],
                        s = constellations[line[0]:line[1], 2],
                        color = 'white',
                        linewidth = 0.5,
                    )
            plt.plot(np.radians(constellations[line[0]:line[1], 0]),
                        constellations[line[0]:line[1], 1],
                        color = 'white',
                        linewidth = 0.5,)
            
        #adding text to constellation a bit to the side if constellation is within plotlimits
        if constellations[line[0], 1] >= 0:
            if previousname != consname[idx]:
                plt.text(np.radians(constellations[line[0], 0])+0.1,
                         constellations[line[0], 1], 
                         consname[idx], 
                         color='aliceblue')
            previousname = consname[idx]
            

    return ax