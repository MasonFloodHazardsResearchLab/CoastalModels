import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4
import os
from utils import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import plotly.offline as po
import pandas as pd
import warnings
from scipy.io import loadmat
warnings.filterwarnings("ignore")
from mpl_toolkits.basemap import Basemap
import pathlib as pl
import glob
import utm
from PIL import Image
from datetime import datetime,timedelta
from mpl_toolkits.mplot3d import Axes3D
import folium 
import branca
from folium.plugins import MeasureControl
import scipy

def utm2geo(x,y,code:int=18,zone:str='northern'):
    limits = x.shape
    x2,y2 = np.ma.array(np.zeros(x.shape)),np.ma.array(np.zeros(y.shape))
    for i in range(0,limits[0]):
        for ii in range(0,limits[1]):
            coord = utm.to_latlon(x[i,ii],y[i,ii],code,zone)
            x2[i,ii] = coord[1] 
            y2[i,ii] = coord[0]
    return x2,y2

def map_plot(x,y,z,data,time,title,levels,lat1:float,lat2:float,lon1:float,lon2:float,label:str='elevation(m)',figsize=(18,10),cmap='jet',save='xbeach.gif'):
  wl=[]
  data[data.mask]=np.nan
  for i in range(0,len(time)):
    file_number = '%05d'%i
    fig,ax = plt.subplots(figsize=figsize)
    data[data <=z+0.00001] = np.nan
    wl.append('WL{}.png'.format(file_number))
    plt.contourf(x,y,data[i,:,:],levels=levels,cmap=cmap,shading='gouraud',vmin=np.min(levels),vmax=np.max(levels),aspect='auto')
    m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,
                        urcrnrlon=lon2,resolution='h', epsg = 4269)
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 600, verbose= False)
    cb = plt.colorbar(cmap=cmap,fraction=0.026,pad=0.04) 
    cb.set_label(label,fontsize=10)
    ax.autoscale_view(tight=True)
    plt.title(title + str(i))
    plt.savefig('WL{}.png'.format(file_number),dpi=400,bbox_inches = 'tight', pad_inches = 0.1)
    plt.close()
    images = []
  for ii in range(0,len(wl)):
      frames = Image.open(wl[ii])
      images.append(frames)
  images[0].save(save,
     save_all=True,
     append_images=images[1:],
     delay=.1,
     duration=300,
     loop=0)
  for f in glob.glob('WL*'):
      os.remove(f) 



  return

def map_velocity(x,y,data,u_velocity,v_velocity,start,time,title,levels,lat1:float,lat2:float,lon1:float,lon2:float,label:str='elevation(m)',figsize=(18,10),gridspace=150,cmap='jet',save='xbeach_velocity.gif'):
    wl=[]
    data[data.mask]=np.nan
    start_date = datetime.strptime(start,'%Y%m%d%H')
    xs,ys = x.shape
    xx = x.reshape((xs*ys))
    yy = y.reshape((xs*ys))
    xg = np.linspace(lon1,lon2,gridspace)
    yg = np.linspace(lat1,lat2,gridspace)
    xgrid,ygrid = np.meshgrid(xg,yg)
    for i in range(0,time):
        u1 = u_velocity[i,:,:]
        v1 = v_velocity[i,:,:]
        uu = u1.reshape((xs*ys))
        vv = v1.reshape((xs*ys))
        ugrid = scipy.interpolate.griddata((xx,yy),uu,(xgrid,ygrid),method='nearest')
        vgrid = scipy.interpolate.griddata((xx,yy),vv,(xgrid,ygrid),method='nearest')
        file_number = '%05d'%i
        fig,ax = plt.subplots(figsize=figsize)
        wl.append('WL{}.png'.format(file_number))
        plt.contourf(x,y,data[i,:,:],levels=levels,cmap=cmap,shading='gouraud',vmin=np.min(levels),vmax=np.max(levels),aspect='auto')
        m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,
                            urcrnrlon=lon2,resolution='h', epsg = 4269)
        m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 400, verbose= False)
        cb = plt.colorbar(cmap=cmap,fraction=0.026,pad=0.04) 
        cb.set_label(label,fontsize=10)
        plt.quiver(xgrid,ygrid,ugrid,vgrid, pivot='mid',scale=1200,scale_units='xy', color='#b3b3b3')
        ax.autoscale_view(tight=True)
        plt.title(title + str(start_date+ timedelta(minutes=i*20)))
        plt.savefig('WL{}.png'.format(file_number),dpi=400,bbox_inches = 'tight', pad_inches = 0.1)
        plt.close()
    images = []
    for ii in range(0,len(wl)):
        frames = Image.open(wl[ii])
        images.append(frames)
    images[0].save(save,
        save_all=True,
        append_images=images[1:],
        delay=.1,
        duration=300,
        loop=0)
    for f in glob.glob('WL*'):
       os.remove(f) 
    return

def contour_map(x,y,z,data,title,levels,lat1:float,lat2:float,lon1:float,lon2:float,label:str='elevation(m)',figsize=(18,10),cmap='jet'):
    #if data.mask:
    data[data.mask]=np.nan
    fig,ax = plt.subplots(figsize=figsize)
    plt.contourf(x,y,data,levels=levels,cmap=cmap,shading='gouraud',vmin=np.min(levels),vmax=np.max(levels),aspect='auto')
    m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,
                        urcrnrlon=lon2,resolution='h', epsg = 4269)
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 600, verbose= False)
    cb = plt.colorbar(cmap=cmap,fraction=0.026,pad=0.04) 
    cb.set_label(label,fontsize=10)
    ax.autoscale_view(tight=True)
    plt.title(title)
    return plt.show()

def find_node_ak(x,y,obs_lat,obs_lon):
    min_distance = 30
    best_x = 0
    best_y = 0
    x1,y1 = x.shape
    for i in range(0,x1):
        for ii in range(0,y1):
            current_distance = (y[i][ii] - obs_lat)**2 + (x[i][ii] - obs_lon)**2
            if min_distance is None or current_distance < min_distance:
                best_x = i
                best_y = ii
                min_distance = current_distance
    #print("best_index:{} ".format(best_index))
    return best_x,best_y

def correct_hobo(mat_file):
    df1 = loadmat(mat_file)
    stat = ['S1','S2','S3','S4']
    data = []
    hobo = pd.DataFrame()
    for ii in range(0,len(stat)):
        dx,dt = [],[]
        wl = df1[stat[ii]]['height_NAVD88'][0][0].tolist()
        time = df1[stat[ii]]['time_NAVD88_cor'][0][0].tolist()
        for i2 in range(0,len(wl)):

            dx.append(float(wl[i2][0])-.75)

            dt.append(time[i2][0])
        for i in range(0,len(dx)-1):
            if dx[i+1]==dx[i] or dx[i]>1.75:
                dx[i]='NaN'
        water = pd.Series(dx)   
        timedepth = pd.to_datetime(pd.Series(dt)-719529, unit='D')
        #if ii == 0:
        hobo[stat[ii]+'_datetime'] = timedepth
        hobo[stat[ii]] = water

    return hobo

def contour_stations(x,y,data,obs_timeseries,obs_locx,obs_locy,model_timeseries,t_start,time,title,levels,
  lat1:float,lat2:float,lon1:float,lon2:float,label:str='elevation(m)',figsize=(18,10),cmap='jet',save='xbeach2d.gif'):
    data[data.mask]=np.nan
    wl=[]
    start_date = datetime.strptime(t_start,'%Y%m%d%H')
    for i in range(0,time):
        file_number = '%05d'%i
        fig = plt.figure(figsize=figsize)
        ax1 = plt.axes([0,0,0.6,1])
        ax2 = plt.axes([0.65,0.75,.55,.1])
        ax3 = plt.axes([0.65,0.55,.55,.1])
        ax4 = plt.axes([0.65,0.35,.55,.1])
        ax5 = plt.axes([0.65,0.15,.55,.1])
        wl.append('WL{}.png'.format(file_number))
        for ii in range(0,4):
            ax1.scatter(x[obs_locx[ii]][obs_locy[ii]],y[obs_locx[ii]][obs_locy[ii]],color='#ff00ff',s=200,zorder=4)
        ax1.contourf(x,y,data[i,:,:],levels=levels,cmap='jet',shading='gouraud',vmin=np.min(levels),vmax=np.max(levels),aspect='auto')
        m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,
                      urcrnrlon=lon2,resolution='h', epsg = 4269,ax=ax1)
        m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 400, verbose= False)
        ax2.plot((model_timeseries['date time'][i],model_timeseries['date time'][i]),(-5,5),'k')
        ax3.plot((model_timeseries['date time'][i],model_timeseries['date time'][i]),(-5,5),'k')
        ax4.plot((model_timeseries['date time'][i],model_timeseries['date time'][i]),(-5,5),'k')
        ax5.plot((model_timeseries['date time'][i],model_timeseries['date time'][i]),(-5,5),'k')
        s1 = ax2.plot(pd.to_datetime(obs_timeseries['S1_datetime']),obs_timeseries['S1'],color='#0099cc')
        s2 = ax3.plot(pd.to_datetime(obs_timeseries['S2_datetime']),obs_timeseries['S2'],color='#0099cc')
        s3 = ax4.plot(pd.to_datetime(obs_timeseries['S3_datetime']),obs_timeseries['S3'],color='#0099cc')
        s4 = ax5.plot(pd.to_datetime(obs_timeseries['S4_datetime']),obs_timeseries['S4'],color='#0099cc')
        model1 = ax2.plot(model_timeseries['date time'],model_timeseries['s1'],'k')
        model2 = ax3.plot(model_timeseries['date time'],model_timeseries['s2'],'k')
        model3 = ax4.plot(model_timeseries['date time'],model_timeseries['s3'],'k')
        model4 = ax5.plot(model_timeseries['date time'],model_timeseries['s4'],'k')
        ax2.set_xlim([start_date,model_timeseries.iloc[-1]['date time']])
        ax3.set_xlim([start_date,model_timeseries.iloc[-1]['date time']])
        ax4.set_xlim([start_date,model_timeseries.iloc[-1]['date time']])
        ax5.set_xlim([start_date,model_timeseries.iloc[-1]['date time']])
        #cb = plt.colorbar(cmap='jet',fraction=0.026,pad=0.04) 
        #cb.set_label('elevation (m)',fontsize=10)
        ax2.set_ylim([-.2,1])
        ax3.set_ylim([-.2,1])
        ax4.set_ylim([-.2,1])
        ax5.set_ylim([-.2,1])

        ax2.set_title('station1')
        ax3.set_title('station2')
        ax4.set_title('station3')
        ax5.set_title('station4')
        ax5.legend(('Obs Station','model station'),
            loc='upper center',bbox_to_anchor=(0.5,-0.2),frameon=False,ncol=8)
        #ax2.set_xticks()
        ax1.set_title((title+str(start_date+ timedelta(minutes=i*20))))
        plt.savefig('WL{}.png'.format(file_number),dpi=300,bbox_inches = 'tight', pad_inches = 0.1)    
        plt.close()
    images = []
    for ii in range(0,len(wl)):
        frames = Image.open(wl[ii])
        images.append(frames)
    images[0].save(save,
        save_all=True,
        append_images=images[1:],
        delay=.1,
        duration=250,
        loop=0)
    for f in glob.glob('WL*'):
        os.remove(f)  
    #plt.show()

    return

def video_3d(x,y,z,data,t_start,time,title,levels,label:str='elevation(m)',figsize=(18,10),save='xbeach3d.gif'):
    from mpl_toolkits.mplot3d import Axes3D
    data[data.mask]=np.nan
    wl = []
    start_date = datetime.strptime(t_start,'%Y%m%d%H')
    for i in range(0,time):
        file_number = '%05d'%i
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        original = ax.plot_surface(x,y,z[i,:,:],cmap='gist_earth',vmin=-1.,vmax=2,antialiased=False, shade=False)
        #water = ax.plot_surface(x,y,zs[i,:,:],color='#3333ff',antialiased=False, shade=False)
        waves = ax.plot_surface(x,y,data[i,:,:],cmap='cool', rstride=1, cstride=1,vmin=-.2,vmax=2,antialiased=False, shade=True)
        wl.append('WL{}.png'.format(file_number))
        ax.set_zlim(-1, 3)
        ax.view_init(30,azim=235)
        ax.autoscale_view(tight=True)
        ax.set_title(title+str(start_date+ timedelta(minutes=i*20)))
        ax.set_ylim(np.min(y)+0.002,np.max(y)-0.002)
        ax.set_xlim(np.min(x)+0.002,np.max(x)-0.002)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig('WL{}.png'.format(file_number),dpi=300,bbox_inches = 'tight', pad_inches = 0.1)
        plt.close()
    images = []
    for ii in range(0,len(wl)):
        frames = Image.open(wl[ii])
        images.append(frames)
    images[0].save(save,
       save_all=True,
       append_images=images[1:],
       delay=.1,
       duration=200,
       loop=0)
    for f in glob.glob('WL*'):
        os.remove(f)
    return

def getColor(x):
    if x < -3:
        color = '#8000FF'
    elif x < -2.5:
        color = '#5500FF'
    elif x < -2:
        color = '#4000FF'
    elif x < -1.5:
        color = '#1500FF'
    elif x < -1:
        color = '#0000FF'
    elif x < -0.5:
        color = '#002AFF'
    elif x < 0:
        color = '#0055FF'
    elif x < 0.5:
        color = '#0080FF'
    elif x < 1:
        color = '#00AAFF'
    elif x < 1.5:
        color = '#00D4FF'
    elif x < 2:
        color = '#00FFFF'
    elif x < 2.5:
        color = '#00FFAA'
    elif x < 3:
        color = '#00FF80'
    elif x < 7:
        color = '#00FF2A'
    elif x < 7.5:
        color = '#2AFF00'
    elif x < 8:
        color = '#80FF00'
    elif x < 8.5:
        color = '#AAFF00'
    elif x < 9:
        color = '#D4FF00'
    elif x < 9.5:
        color = '#FFFF00'
    elif x < 10:
        color = '#FFD400'
    elif x < 10.5:
        color = '#FFAA00'
    elif x < 11:
        color = '#FF8000'
    elif x < 11.5:
        color = '#FF6A00'
    elif x < 12:
        color = '#FF4000'
    elif x < 12.5:
        color = '#FF2A00'
    elif x < 13:
        color = '#FF1500'
    elif x < 13.5:
        color = '#FF0000'
    else:
        color = '#FF0000'
    return color 

def interactive_grid(centery, centerx, lat, lon, z):

    url_base = 'http://server.arcgisonline.com/ArcGIS/rest/services/'
    service = 'World_Imagery/MapServer/tile/{z}/{y}/{x}'
    tileset = url_base + service
    folmap = folium.Map( location=[centery, centerx],zoom_start=10) #width=800, height=600,
    x1,y1 = lat.shape

    for i in range(0,x1):
        for ii in range(0,y1):
            folmap.add_child(folium.CircleMarker(location=[lat[i][ii],lon[i][ii]],radius=1,
                                                 weight=1,fill=True, color=getColor(z[i][ii]),fill_color=getColor(z[i][ii]), fill_opacity=1))
    colormap = branca.colormap.StepColormap(colors=['#8000FF','#5500FF','#4000FF','#1500FF','#0000FF','#002AFF','#0055FF','#0080FF','#00AAFF','#00D4FF','#00FFFF',
                                                    '#00FFAA','#00FF80','#00FF2A','#2AFF00','#80FF00','#AAFF00','#D4FF00','#FFFF00','#FFD400','#FFAA00','#FF8000',
                                                    '#FF6A00','#FF4000','#FF2A00','#FF1500','#FF0000'],vmin=-3,vmax=1)
    #colormap = colormap.to_step(index=[0, 0.5,1,1.5,2,2.5,3,3.5,4,4.5,5])
    colormap.caption = 'Elevation (m) at NAVD88'
    colormap.add_to(folmap)
    #my_ip = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4').content.decode()a

    #folium.TileLayer(tiles='http://{}:{}/tile/{{z}}/{{x}}/{{y}}.png', 
    #             attr='GeoPySpark', name='NED_SC', overlay=True).add_to(folmap)
    #folium.add_tiles(folmap)

    folium.TileLayer(tileset, attr="ESRI", name='imagery').add_to(folmap)
    folium.LayerControl().add_to(folmap)
    folmap.add_child(MeasureControl())

    return folmap










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


