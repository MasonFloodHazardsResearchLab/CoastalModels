import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4
import os
from utils import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.figure_factory as ff
#from IPython.display import HTML
import plotly.graph_objs as go
import plotly.offline as po
import pandas as pd
import warnings
from scipy.io import loadmat
warnings.filterwarnings("ignore")
from mpl_toolkits.basemap import Basemap
import pathlib as pl

def hobo(mat_file):
    df1 = loadmat(mat_file)
    stat = ['S1','S2','S3','S4']
    data = []
    for ii in range(0,1):
        dx,dt = [],[]
        wl = df1[stat[ii]]['height_NAVD88'][0][0].tolist()
        time = df1[stat[ii]]['time_NAVD88_cor'][0][0].tolist()
        for i2 in range(0,len(wl)):

            dx.append(float(wl[i2][0]))

            dt.append(time[i2][0])
        for i in range(0,len(dx)-1):
            if dx[i+1]==dx[i] or dx[i]>1.75:
                dx[i]='NaN'
        water = pd.Series(dx)   
        timedepth = pd.to_datetime(pd.Series(dt)-719529, unit='D')
        hobo = pd.DataFrame({'datetime':timedepth,'water level (m) NAVD88':water})

    return hobo

def adcp(files1):
    t2 = loadmat(files1)
    h02 = t2['H0'][0]
    tp2 = t2['Tp'][0]
    depth2 = t2['Depth'][0]
    total_pr2 = t2['Total_Pr']
    total_pr_m2= t2['Total_Pr_m'][0]
    timedepth2 = pd.to_datetime(t2['timedepth3'][0]-719529, unit='D')
    df2 = pd.DataFrame({'datetime':timedepth2,'h0':h02,'Tp':tp2,'depth':depth2})
    return df2

def trublues(file):
    t1 = loadmat(file)
    h01 = t1['H0'][0]
    tp1 = t1['Tp'][0]
    depth1 = t1['Depth'][0]
    total_pr1 = t1['Total_Pr']
    total_pr_m1= t1['Total_Pr_m'][0]
    timedepth1 = pd.to_datetime(t1['timedepth3'][0]-719529, unit='D')
    df = pd.DataFrame({'datetime':timedepth1,'h0':h01,'Tp':tp1,'depth':depth1})
    return df 

def write_waves(root_dir,h0,Tp,duration,period,mainang=90.0,gammajsp=3.3,s=10.0,fnyq=0.45,timestep=1.0):
    root_dir = pl.Path(root_dir)
    data = []
    y = 0
    data.append('FILELIST'+'\n')
    for i in range(1,int(period/duration)):
        with open(str(root_dir /f'jonswap_{i}.txt'),'w') as fin:
            fin.write('Hm0           = {:.4e}'.format(h0[y])+ '\n' +
                      'fp            = {:.4e}'.format(float(1/Tp[y]))+ '\n' +
                      'mainang       = {:.4e}'.format(mainang) + '\n' +
                      'gammajsp      = {:.4e}'.format(gammajsp) + '\n' +
                      's             = {:.4e}'.format(s) + '\n' +
                      'fnyq          = {:.4e}'.format(fnyq) + '\n')
            data.append(f'    {duration}    {timestep}   jonswap_{i}.txt'+'\n')
        y+=1
    with open(str(root_dir / 'filelist.txt'),'w') as control:
        lines = control.writelines(data)
    return

def write_tide(root_dir,time,front,back):
    root_dir = pl.Path(root_dir)
    file = root_dir / 'tide.txt'
    data = []
    for i in range(0,len(time)):
        if float(front[i])/float(front[i]) != 1:
            if float(front[i-1])/float(front[i-1]) != 1:
                front[i] = 0.5
            else:
                front[i] = front[i-1]
         #   front[i] = 0
         #  back[i] = 0
        data.append('    {:.4e}    {:.4e}    {:.4e}'.format(float(time[i]),float(front[i]),float(front[i])) + '\n')
        #data.append('    {:.4e}    {:.4e}    {:.4e}'.format(float(time[i]),float(front[i])*1.5,float(back[i])*1.5) + '\n')
    with open(file,'w') as fin:
        fin.writelines(data)
    return

def write_vege_map(path:str,bathy_file:str,fname:str='vege_map.txt',elevation:float=0.05):
    path = pl.Path(path)
    with open(str(path / bathy_file),'r+') as fin:
        with open(str(path / fname),'w+') as fout:
            lines = fin.readlines()
            for line in lines:
                data = line.strip().split('  ')
                for i in range(0,len(data)):
                   # print(data)
                    vege = []
                    new = []
                    if data != '':            
                        if float(data[i]) > elevation:
                            fout.write('   '+str(1))
                        else:
                            fout.write('   '+str(0))
                fout.write('\n')
    return






'''
frames = []
x = xb.variables['globalx'][:,:][0]
data = [dict(x=x, y=x*0+-5,
           name='topo',mode='lines',legendgroup='b',line=dict(width=2, color='white')),
        dict(x=x, y=xb.variables['H_mean'][0,:][0]+xb.variables['zs_mean'][0,:][0],
           name='waves',mode='lines',legendgroup='b',line=dict(width=2, color='#3399ff')),
       dict(x=x, y=xb.variables['zs_mean'][0,:][0],
           name='water depth',mode='lines',legendgroup='a',line=dict(width=2, color='blue')),
       dict(x=x, y=xb.variables['zb_mean'][0,:][0],
           name='topo/bathy',mode='lines',line=dict(width=2, color='grey'),
           fill='tonexty',fillcolor='blue'),
       ]
            #fill='tozeroy',fillcolor='#737373'),
       # dict(x=x, y=xb.variables['zb_mean'][0,:][0],
       #    mode='lines',legendgroup='a',showlegend= False,line=dict(width=2, color='#737373'),
       #     fill='tonexty',fillcolor='blue')]#,
        #dict(x=x, y=xb.variables['zs_mean'][0,:][0],
        #   name=None,mode='lines',legendgroup='b',showlegend= False,line=dict(width=2, color=None),
        #    fill='tonexty',fillcolor='cyan')]

    
frames=[dict(data=[dict(x=x, y=xb.variables['H_mean'][k,:][0]+xb.variables['zs_mean'][k,:][0], 
                        mode='lines',line=dict(color='#3399ff', width=2),),
                   dict(x=x, y=xb.variables['zs_mean'][k,:][0], 
                        mode='lines',line=dict(color='blue', width=2)),
                   dict(x=x, y=xb.variables['zb_mean'][k,:][0], 
                        mode='lines',line=dict(color='grey', width=2),
                        fill='tonexty',fillcolor='blue'),
                    dict(x=x, y=x*0+-3, 
                        mode='lines',line=dict(color='white', width=2),
                        fill='tonexty',fillcolor='grey')
                  # dict(x=x, y=xb.variables['zb_mean'][k,:][0],
                  #      mode='lines',legendgroup='a',showlegend= False,line=dict(color='blue', width=2)),
                  #  dict(x=x, y=xb.variables['zs_mean'][k,:][0],name=None,mode='lines',
                  #       legendgroup='b',showlegend= False,line=dict(width=2, color=None))
                  ]) for k in range(0,len(t))]    

sliders=[dict(steps=[dict(method='animate',args= [
                    dict(mode='immediate',frame= dict(duration=len(t), redraw= False),
                    transition=dict(duration=len(t),steps= []))],
                    label='{:d}'.format(k+1)) for k in range(len(t))],
                    transition= dict(duration=len(t)),x=0.01,y=0, 
        currentvalue=dict(font=dict(size=12), 
                          prefix='Time step: ', visible=True, 
                          xanchor='center'),len=1.0)]
layout=dict(width=1100, height=500,
            xaxis=dict(range=[0, 104],zeroline=False,showline=False),yaxis=dict(range=[-.5, 4]),
              title='XBeach', hovermode='closest',
            updatemenus= [{'type': 'buttons','buttons': [{'label': 'Play',
                        'method': 'animate','args': [None, {'frame': {'duration': 1000, 'redraw': False},
                         'fromcurrent': True, 'transition': {'duration': 100, 'easing': 'quadratic-in-out'}}]},
                        {'label': 'Pause','method': 'animate','args': [[None], {'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate','transition': {'duration': 0}}]}],'direction': 'left','pad': {'r': 10, 't': 87},
                        'showactive': False,'type': 'buttons','x': 0.1,'xanchor': 'right','y': -0.05,'yanchor': 'top'}],sliders=sliders)  

figure=dict(data=data,layout=layout, frames=frames)          
po.plot(figure,'xbeach_animation.html')
iplot(figure)
'''


