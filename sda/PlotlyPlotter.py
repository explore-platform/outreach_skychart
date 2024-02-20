#Plotly Imports
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
pio.renderers.default='browser'

def create_plotly(dust_data, solarsystem, constellations, constellationinfo, consname):
    fig = go.Figure()
    
    #Extract columns because to meet requirements of Plotly 
    altitude_column = dust_data['alt'].deg.flatten()
    azimuth_column = dust_data['az'].deg.flatten()
    magnitude = dust_data['data'].flatten()
    markersizes = magnitude*2 #Make the size of the markers scale with magnitude
    
    #General layout
    fig.update_layout(
        #title = 'Night Sky Map',
        margin = dict(t = 0),
        showlegend = False)
    
    
    
    #Plot extinction values
    fig.add_trace(go.Scatterpolargl(theta= azimuth_column, 
                                    r= altitude_column, 
                                    marker = dict(size = markersizes,
                                                  symbol = 'circle',
                                                  color = magnitude,
                                                  colorscale= 'inferno', #'agsunset',
                                                  line = dict(width = 0),
                                                  colorbar = dict(bordercolor = '#fff',
                                                                  len = 600, 
                                                                  lenmode = 'pixels',
                                                                  ticksuffix = ' mag',
                                                                  title = dict(text = 'Extinction level (10log)'),
                                                                  xpad = 80
                                                                  )
                                                  ),
                                    mode = 'markers'))
    
    #fig.update_coloraxes(xpad = 20)
    
    #Create further layout (orientation, labels etc)
    fig.update_polars(dict(angularaxis = dict(rotation = 90,
                                              direction = 'counterclockwise',
                                              tickmode = 'array',
                                              tickvals = [0,45, 90,135,180,225,270,315],
                                              ticktext = ['N - 0°', 'NE - 45°','E - 90°', 'SE - 135°', 'S - 180°', 'SW - 225°', 'W - 270°', 'NW - 315°'],
                                              tickfont = dict(family = 'Geometria',
                                                              size = 18,
                                                              color = 'rgb(83, 73, 152)')
                                              ),
                                             
        
                           radialaxis = dict(range = [90,0],
                                             color = '#ECECEC',
                                             ticksuffix = '°', 
                    
                                            ),
                           
                            bgcolor = '#041A40'                 
                         ),
                  
                      )


    #Plotting the constellation data
    for idx, line in enumerate(constellationinfo):
        fig.add_trace(go.Scatterpolargl(theta = constellations[line[0]:line[1], 0],
                                      r = constellations[line[0]:line[1], 1],
                                      mode = 'lines+markers', 
                                      marker = dict(size = constellations[line[0]:line[1], 2],
                                                    color = '#fff',
                                                    opacity = 1
                                                    #symbol = 'star'
                                                    ),
                                      line = dict(width = 1),
                                      text = consname[idx],
                                      ))
       
      
     #Redraw axes which are hidden by earlier traces    
    theta = np.linspace(0, 360, 100)
    radii = np.linspace(0, 90, 10)    
    for radius in radii:
        # Making the r=0 line thicker to hide ragged axis 
        if radius == 0:
            fig.add_trace(go.Scatterpolargl(r=[radius]*100,
                                             theta=theta,
                                             mode='lines',
                                             line = dict(width = 6,
                                                         color = "#FFF")
                                             )
                          )
            
        # Drawing the other radii    
        else:
            fig.add_trace(go.Scatterpolargl(r=[radius]*100,
                                            theta=theta,
                                            mode='lines',
                                            line = dict(width = 1,
                                                        color = "#EBEBEB")
                                            )
                          )
             
    #Plotting the solar system data for each body    
    for idx, body in enumerate(solarsystem['body']):
        fig.add_trace(go.Scatterpolargl(theta= solarsystem['az'][idx],
                                        mode = 'markers+text',
                                        r= solarsystem['alt'][idx], 
                                        marker = dict(size = solarsystem['size'][idx],
                                                      color = str(solarsystem['color'][idx])),
                                        text = str(body),
                                        textfont= dict(color = str(solarsystem['color'][idx]),
                                                       size = 13), 
                                        textposition = 'bottom center'))
     
   
                      

    

    return fig 
