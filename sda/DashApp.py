#cd  -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 16:07:53 2023

@author: lgreijn
"""

# version information
__project__ = "EXPLORE"
__author__  = "ACRI-ST"
__modifiers__ = '$Author: L. Greijn $'
__date__ = '$Date: 2023-10-30 $'
__version__ = '$Rev: 1.0 $'
__license__ = '$Apache 2.0 $'

# Import Dash packages
from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_daq as daq
import datetime as d #otherwise it will complain due to 'date' variables and objects
import os 
#Importing Astropy packages
import astropy.units as u
from astropy.coordinates import EarthLocation 
from astropy.time import Time

#Importing functions from other scripts
from integrated_dust_data import getintegratedcoordinates, to_altaz
from constellation_data import query_constellations
from solarsystem import get_solarsystem
from PlotlyPlotter import create_plotly


# Incorporate data
data_location = './data/' #Folder in which datacube is stored
data_name = 'explore_cube_density_values_050pc_v1.h5' #datacube name
file = data_location + data_name #Creating path to datafile 

#Import assets
explore_logo = './assets/Explore_Logo_Standard.png'
EU_flag = './assets/EUflag.png'
table = getintegratedcoordinates()

#Style rules Explore
fonttype = 'Geometria'
EXP_yellow = 'rgb(198, 143, 10)'
EXP_purple = 'rgb(83, 73, 152)'

#Style dictionary text
style_titles = {'font-size' : '25px',
              'font-family' : fonttype, 
              'padding-left': '8px',
              'padding-bottom': '8px',
              'width' :  '100%',
              'display' : 'inline-block',
              'verticalAlign': 'top',
              #'color' : EXP_purple,
              }

style_headers = {'font-size' : '20px',
              'font-family' : fonttype, 
              'padding-left': '8px',
              'padding-bottom': '3px',
              'width' :  '100%',
              'display' : 'inline-block',
              'verticalAlign': 'top',
              #'color' : EXP_purple,
              }

style_text = {'font-size' : '16px',
              'font-family' : fonttype, 
              'display' : 'inline-block',
              'margin' : '7px',
              'verticalAlign': 'bottom',
              }

style_units = {'font-size' : '16px',
              'font-family' : fonttype, 
              'margin' : '7px',
              'width' : '10%',
              'display' : 'inline-block',
              'verticalAlign': 'bottom',
              }

style_inputboxes = {'width' : '8%',
                    'verticalAlign': 'bottom',
                    'display' : 'inline-block',
                    'margin' : '5px'}

# Initialize the app
#app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app = Dash(__name__, #suppress_callback_exceptions=True,
    routes_pathname_prefix=os.environ.get('PATH_PREFIX', '/'),
    requests_pathname_prefix = os.environ.get('PATH_PREFIX', '/'),
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags = [
        {"name": "viewport",
         "content": "width=device-width, initial-scale=1.0"},
    ],
)

app.scripts.config.serve_locally = True
app.title = "EXPLORE: Dusty Sky Charts" 
app.config.suppress_callback_exceptions = True

# App layout
app.layout = html.Div([
    #Page header-----------------------------------------------------------------------------------
    html.Div(
        html.Img(src = explore_logo,
                 style = {'width' : '80%',
                          'margin' : '5px',
                          'display' : 'inline-block',
                          'verticalAlign': 'bottom',
                     }
                 ),
        style = {'width' : '10%',
                 'display' : 'inline-block',
                 'verticalAlign' : 'top'}
            ),
    
    html.Div('Create your own Dusty Sky Chart',
             style = {'font-size' : '40px',
                      'font-family' : fonttype,
                      'width' : '70%',
                      'margin' : '10px',
                      'display' : 'inline-block',
                      'verticalAlign': 'bottom',
                      'color' : EXP_purple
                      }
             ),
    
    #End of page header 

    html.Br(),
    
    #Page contents -------------------------------------------------------------------------------
    
    #Left side of the screen--------------------------------------
    html.Div([
        html.Div([
            html.Div('Inputs',
                     style = style_titles
                     ),
            
            html.Br(),
            html.Br(),
            #Location inputs-----------------------------------------
            #Location Header
            html.Div('Location inputs', 
                     style = style_headers),
            
            #Switch to use user location
            daq.BooleanSwitch(on = False,
                             id = 'location_switch',
                             color = EXP_purple,
                             label = 'Use my current location',
                             labelPosition = 'top',
                             style = {'display' : 'inline-block',
                                      'verticalAlign' :'top',
                                      'font-family' : fonttype,
                                      'font-size' : '10px',
                                      'margin' : '16px'},
                             ),
            
            dcc.Geolocation(id = 'geolocation'
                            ),
            
            html.Br(),
            
            #manual coordinate input 
            html.Div([
                html.Div('Longitude',
                         style = style_text),
                
                dcc.Input(
                    id="long",
                    value=0,
                    type="number",
                    min=-180, max=180,
                    style = style_inputboxes
                    ),
                
                html.Div('deg',
                          style = style_units,
                          ),
                
                html.Div('Latitude',
                          style = style_text,
                          ),
                 
                dcc.Input(id="lat",
                          value=0,
                          type="number",
                          min=-90, max=90,
                          style = style_inputboxes
                          ),
                 
                 html.Div('deg',
                           style = style_units,
                           ),
                
                ]),
                 
            #Text that will display the last used position
            html.Div(id='text_position',
                    style = {
                        'verticalAlign' :'top',
                        'font-family' : fonttype,
                        'font-size' : '13px',
                        'margin' : '8px'}
                    ),
            #End of location inputs
            
            html.Br(),
            html.Br(),
            
            #Time inputs-------------------------------------------------
            html.Div('Time & date inputs', 
                     style = style_headers
                     ),
            html.Br(),
            
            #Date selection---------------------------------------------
            html.Div('Select date', 
                     style = style_text
                     ),
            
            dcc.DatePickerSingle(
                id = 'date_picker',
                min_date_allowed=d.date(1995, 8, 5),
                max_date_allowed=d.date(2040, 12, 31),
                date= d.date.today(), #Date automatically selected
                display_format= 'D-M-Y',
                style = {'width' : '200px',
                         'height' : '25px',
                         'display' : 'inline-block',
                         'verticalAlign': 'top',
                         },
                    	),
            
            #Leaving some spacing due to size of date selector
            html.Br(),
            html.Br(),
            #Time Selection---------------------------------------------
            html.Div(
            [#Input for the Astropy Time computation
                html.Div('Time',
                      style = style_text,
                      ),
             
                dcc.Input(
                    id="hour",
                    value=0,
                    type="number",
                    min=0, max=23,
                    style = style_inputboxes
                    ),
             
                html.Div(':',
                         style = {'font-size' : '16px',
                                  'font-family' : fonttype, 
                                  'margin' : '3px',
                                  'display' : 'inline-block',
                                  'verticalAlign': 'middle',
                                  'padding-bottom' : '5px'
                                  },
                         ),
              
                dcc.Input(id="min",
                          value=0,
                          type="number",
                          min=-0, max=59,
                          style = style_inputboxes
                          ),
                
                html.Div('Timezone',
                       style = style_text,
                       ),
              
                dcc.Dropdown(options ={ '-11' : 'UTC -11',
                                       '-10' : 'UTC -10',
                                       '-9' : 'UTC -9',
                                       '-8' : 'UTC -8',
                                       '-7' : 'UTC -7',
                                       '-6' : 'UTC -6',
                                       '-5' : 'UTC -5',
                                       '-4' : 'UTC -4',
                                       '-3' : 'UTC -3',
                                       '-2' : 'UTC -2',
                                       '-1' : 'UTC -1',
                                       '0' : 'UTC +0',
                                       '1' : 'UTC +1',
                                       '2' : 'UTC +2',
                                       '3' : 'UTC +3',
                                       '4' : 'UTC +4',
                                       '5' : 'UTC +5',
                                       '6' : 'UTC +6',
                                       '7' : 'UTC +7',
                                       '8' : 'UTC +8',
                                       '9' : 'UTC +9',
                                       '10' : 'UTC +10',
                                       '11' : 'UTC +11',
                                       },
                             value='0',
                             style = {'width' : '120px',
                                      'height' : '35px',
                                      'display' : 'inline-block',
                                      'verticalAlign' : 'bottom',
                                      'padding-bottom' : '5px'
                                      },
                             id = 'tz'
                             ),
                
            ]
        ),
        
        html.Br(),
        
        #Submit button--------------------------------------------
        html.Div([
            html.Button('Submit', 
                       id = 'submit_button',
                       n_clicks = 0, 
                       style = {'margin' : '5px',
                                'font-family' : fonttype,
                           },
                ),
            
            #Warning message about computation time
            html.Div('Please be aware that loading the graph may take some time',
                     style = {
                         'display' : 'inline-block',
                         'verticalAlign' :'bottom',
                         'font-family' : fonttype,
                         'font-size' : '13px',
                         'margin' : '8px'})
        
            ]),
        ], 
        #Styling the box around the inputs
        style = {'width' : '100%',
                'display' : 'inline-block',
                #'margin' : '10px',
                'border-style' : 'dotted',
                'border-width' : '2px',
                'border-color' : EXP_yellow,
                'vertical Align' : 'top'}
             ),
        
        #EU Funding acknowledgements
        html.Div([
            html.Img(src = EU_flag,
                     style = {'width' : '60px',
                              'margin' : '5px',
                              'display' : 'inline-block',
                              'verticalAlign': 'top',
                              }
                     ),
            
            html.Div('This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 101004214.',
                     style = {'font-size' : '10px',
                              'font-family' : fonttype, 
                              'display' : 'inline-block',
                              'color' : EXP_yellow,
                              'margin' : '7px',
                              'verticalAlign': 'top',
                                }
                     ),
                ],
            style = {'verticalAlign' : 'top',
                     'display': 'inline-block'}
            ),
            
 
        ],
        #Styling the left side of the screen
        style = {'width' : '30%',
                'display' : 'inline-block',
                'margin' : '10px',
                'verticalAlign' : 'top'}
             ),

    
    
    
    #Right side of the screen-------------------------------------
    html.Div(
        dcc.Loading(children=[
        dcc.Graph(id="skymap", figure={},
                style = {'width' : '1000px',
                         'height' : '850px',
                         'padding_left' : '25px',
                         'verticalAlign' : 'top'}
                )],
                id = 'loading',
                type = 'dot',
                color = EXP_yellow
                ),
             style = {'width' : '65%',
                      'display' : 'inline-block',
                      'margin' : '20px',
                      'verticalAlign' : 'top'
                      }
             ),
 
])

#Application call back functions ---------------------------------------------
@app.callback(
    Output("skymap", "figure"),
    Output('submit_button', 'n_clicks'),
    Output('text_position', 'children'),
    Input('submit_button', 'n_clicks'),
    [State("long", "value"),
    State("lat", "value"),
    State('hour', 'value'),
    State('min', 'value'),
    State('tz', 'value'),
    State('date_picker', 'date'),
    State('geolocation', 'position'),
    State('location_switch', 'on')
    ],
)

#Application computations----------------------------------------------------
def sync_input(clicks, long, lat, hour, minute, tz, date_val, pos, switch_on):
   
    #Ensuring page only updates after the user presses submit
    if clicks == 0 or clicks is None:
        raise PreventUpdate()
    
    
    else: 
        #Check if the user has manually changed the date, otherwise use today
        if date_val is not None:
            date_object = d.date.fromisoformat(date_val)
            date_string = str(date_object.strftime('%Y-%m-%d'))
        else:
            date_object = d.date.today()
            date_string = str(date_object.strftime('%Y-%m-%d'))
         
        #Check if user selected their current geolocation or not and assign coordiantes    
        if switch_on == True:
            text = f"Your current coordinates are lat {pos['lat']}, lon {pos['lon']}, with an accuracy of {pos['accuracy']} meters",
            lat = pos['lat']
            long = pos['lon']
        else:
            text = f'Your selected location was lat {lat} [deg], lon {long} [deg]'
            
        #Convert inputted time to Astropy Time function 
        print('Interpreting the inputs')
        time_string = str(date_string + ' ' + str(hour)+ ':' + str(minute)+ ':00') #Extract inputted time
        utcoffset = int(tz)*u.hour  #Extract selected timezone
        obs_time = Time(time_string) - utcoffset #Create Time object
        
        print('finding earth location')
        #Extract selected location to Astropy EarthLocation object
        obs_loc = EarthLocation(lat=lat*u.deg, lon=long*u.deg)
        
        #Generate the data to be plotted 
        print('generating dust data')
        dust_data = to_altaz(table, obs_loc, obs_time) #Gather extinction data
        print('generating solar system data')
        solarsystem = get_solarsystem(obs_loc, obs_time) #Gather solar system data
        print('generating constellation data')
        constellations, constellationinfo, consname = query_constellations(obs_loc, obs_time) #Gather constellation data
        
        #Create plot using Plotly
        fig = create_plotly(dust_data, solarsystem, constellations, constellationinfo, consname)
        
    #Return required arguments
    return  fig, clicks, text


server=app.server

# Run the app
if __name__ == '__main__':
    try:
        # Config if we want to bootup dash's built-in dev server, hot reload doesn't seem to work however
        app.run_server(
            host='0.0.0.0', debug=True, port=8050, threaded=False
            # , processes=4
        )
        
        # Config when run with gunicorn 
        # app.run(host='0.0.0.0', debug=True, port=8050)
        
    except Exception as e:
        print(e)