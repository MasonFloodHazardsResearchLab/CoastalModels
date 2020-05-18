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
import numpy as np

def write_waves(root_dir,h0,Tp,duration,period,mainang=90.0,gammajsp=3.3,s=10.0,fnyq=0.45,timestep=1.0):
	root_dir = pl.Path(root_dir)
	data = []
	y = 0
	data.append('FILELIST'+'\n')
	for i in range(1,int(period/duration)):
		with open(str(root_dir / f'jonswap_{i}.txt'),'w') as fin:
			fin.write('Hm0           = {:.4e}'.format(h0[y])+ '\n' +
					  'fp            = {:.4e}'.format(float(1/Tp[y]))+ '\n' +
					  'mainang       = {:.4e}'.format(mainang) + '\n' +
					  'gammajsp      = {:.4e}'.format(gammajsp) + '\n' +
					  's             = {:.4e}'.format(s) + '\n' +
					  'fnyq          = {:.4e}'.format(fnyq) + '\n')
			data.append(f'    {duration}    {timestep}    jonswap_{i}.txt'+'\n')
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
		if float(back[i])/float(back[i]) != 1:
			if float(back[i-1])/float(back[i-1]) != 1:
				back[i] = 0.5
			else:
				back[i] = back[i-1]				
		 #   front[i] = 0
		 #  back[i] = 0
		data.append('    {:.4e}    {:.4e}    {:.4e}'.format(float(time[i]),float(front[i]),float(back[i])) + '\n')
		#data.append('    {:.4e}    {:.4e}    {:.4e}'.format(float(time[i]),float(front[i]),float(back[i])*1.5) + '\n')
	with open(file,'w') as fin:
		fin.writelines(data)
	return

def write_2delft(path:str,array:np.array,filename:str):
	xx,yy = array.shape
	nl = '\n'
	lines = np.ceil(yy/12)
	with open(str(path / filename),'w') as fin:
		for i in range(xx):
			for ii in range(yy):
				if ii%12 == 0:
					fin.write(nl + '   ' + '{:0.4e}'.format(array[i,ii]))				
				fin.write('   ' +  '{:0.4e}'.format(array[i,ii]))
	return

def frict_locator(path:str,grid_x:np.array, grid_y:np.array, elevation:np.array, v_types:list=[1,2,3,0],mannings:list=[0.027,0.02,0.025,0.100]):
    xx,yy = grid_x.shape
    vege = np.zeros((xx,yy))
    bed  = np.zeros((xx,yy))
    z0 = elevation
    for i in range(0,xx):
        for ii in range(0,yy):
            if z0[i,ii] < -.01 and grid_x[i,ii] > -75.955 and grid_y[i,ii] < 38.1485:
                bed[i,ii] = mannings[0]
            elif .05 < z0[i,ii] < 0.6 and -75.955 < grid_x[i,ii] < -75.954 and 38.1487< grid_y[i,ii] < 38.1495:
                vege[i,ii] = v_types[1]
            elif z0[i,ii]<-.01 and grid_x[i,ii]>-75.95325:
                bed[i,ii] = mannings[0]
            elif -0.05<z0[i,ii]<0.7 and grid_x[i,ii]>-75.955:
                bed[i,ii] = mannings[2]
                vege[i,ii]=v_types[0]
            elif z0[i,ii]>0.7:
                bed[i,ii] = mannings[3]
                vege[i,ii]=v_types[2]
            else:
                bed[i,ii] = mannings[1]
                vege[i,ii]=v_types[3]
    return vege,bed

def init_zsinit(path:str,z:np.array,zs:np.array):
	xx,yy = z.shape
	zinit = np.ma.array(np.zeros((xx,yy)))

	for i in range(xx):
		for ii in range(yy):
			if z[i,ii] >= 0:
				zinit[i,ii] = 0
			else:
				zinit[i,ii] = zs[i,ii]
	return zinit
