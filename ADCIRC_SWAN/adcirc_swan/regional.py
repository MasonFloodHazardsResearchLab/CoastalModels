
from math import cos, sin, asin, sqrt, radians
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4
import os
#from adcirc import adcirc as adc
#import swan
import matplotlib.pyplot as plt
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from IPython.display import HTML
import plotly.graph_objs as go
import plotly.offline as po
import pandas as pd
import requests


def find_wave_buoy(year,lat1,lat2,lon1,lon2,kml_path) -> dict : 
    '''
    function to find all buoys within bounding box for a specific year
    need to have the wave_buoy file
    '''
    file = pd.read_csv(kml_path / 'wave_buoys.csv')
    buoys = []

    for i in range(len(file)):
        if (lon1<file['X'][i]<lon2) & (lat1<file['Y'][i]<lat2):
            buoys.append(i)
    
    data = {'DateTime':[],'WVHT':[],'Name':[],'Loc':[]}
    for p in buoys:
        station = file['Name'][p]
        try:
            url = f'https://www.ndbc.noaa.gov/view_text_file.php?filename={station}h{str(year)}'\
            		'.txt.gz&dir=data/historical/stdmet/'
            obs_wh = pd.read_csv(url,sep='\s+').drop(index=0).reset_index()
            obs_wh['DateTime'] = pd.to_datetime(obs_wh['#YY']+obs_wh['MM']+obs_wh['DD']+
                                                obs_wh['hh']+obs_wh['mm'],
                                                yearfirst=True,format='%Y%m%d%H%M')
            
            obs_wh = obs_wh.drop(columns=['index','#YY','MM','DD','hh','mm'])
            obs_wh[(obs_wh['WVHT'].astype(float)>=40) | (obs_wh['WVHT'].astype(float)<0)] = np.nan
            data['DateTime'].append(obs_wh['DateTime'])
            data['WVHT'].append(obs_wh['WVHT'].astype(float))
            data['Name'].append(file['Snippet'][p])
            data['Loc'].append([file['Y'][p],file['X'][p]])
        except:
            pass
    return data

def noaa_data(begin,end,station,vdatum='NAVD',interval='6',
                       form='json',t_zone='GMT',unit='metric',product='water_level'):
    api = f'https://tidesandcurrents.noaa.gov/api/datagetter?begin_date={begin}&end_date={end}&station={station}'\
         f'&product={product}&application=NOS.COOPS.TAC.WL&datum={vdatum}&time_zone={t_zone}&units={unit}&format={form}'
    data = requests.get(url=api).content.decode()
    return data
