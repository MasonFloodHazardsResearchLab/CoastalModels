############################################################################################################
## Wave Transformation Tool / Pre-Processing of max waves and water levels
############################################################################################################
## Author: F. Cassalho
## Version: ArcMap 10.5.X
## Inputs: ADCIRC+SWAN max outputs (Direction, Magnitude, Total Water Levels)
## Output: Table with the extracted info
## Date: 5/20/2021
############################################################################################################


# Import libraries 
import netCDF4 as nc4
import pandas as pd
import arcpy
import time

# Launch Console and Start timming
arcpy.AddMessage("Start working...")
startTime = time.clock()


# Setting the input and output files and folders
f_DIR_MAX = nc4.Dataset(arcpy.GetParameterAsText(0))
f_HS_MAX = nc4.Dataset(arcpy.GetParameterAsText(1))
f = nc4.Dataset(arcpy.GetParameterAsText(2))

N = arcpy.GetParameterAsText(3)
S = arcpy.GetParameterAsText(4)
E = arcpy.GetParameterAsText(5)
W = arcpy.GetParameterAsText(6)

OUTPUT_FILE = arcpy.GetParameterAsText(7) 


try:
    # Extracting max water levels
    zeta = f.variables['zeta_max'][:]
    zeta = pd.DataFrame(zeta.data)
    zeta= zeta.values.tolist()
    new_zeta=[]
    for i in zeta[:]:
        new_zeta.append(i[0])
    arcpy.AddMessage("Max water levels extracted...")

    time = f.variables['time_of_zeta_max'][:]
    time = pd.DataFrame(time.data)
    time= time.values.tolist()
    new_time=[]
    for i in time[:]:
    	new_time.append(i[0])
    arcpy.AddMessage("Time of max water level extracted...")

    # Extracting max significant wave height
    w_mag = f_HS_MAX.variables['swan_HS_max'][:]
    w_mag = pd.DataFrame(w_mag.data)
    w_mag = w_mag.values.tolist()
    new_w_mag = []
    for i in w_mag[:]:
        new_w_mag.append(i[0])
    arcpy.AddMessage("Max Hs extracted...")
        
    # Extracting wave direction in the time of max
    w_dir = f_DIR_MAX.variables['swan_DIR_max'][:]
    w_dir = pd.DataFrame(w_dir.data)
    w_dir = w_dir.values.tolist()
    new_w_dir = []
    for i in w_dir[:]:
        new_w_dir.append(i[0])
    arcpy.AddMessage("Max wave direction extracted...")

    # Creating nodes IDs
    node=[]
    for i in range(1, len(zeta)+1):
        node.append(i)
        
    # Extracting longitude
    lon = f.variables['x'][:]
    lon = lon.tolist()
    new_long = []
    for i in lon[:]:
        new_long.append(i)

    # Extracting latitude
    lat = f.variables['y'][:]
    lat = lat.tolist()
    new_lat = []
    for i in lat[:]:
        new_lat.append(i)
    arcpy.AddMessage("Node coordinates extracted...")

    # Compiling the extracted information into a single file
    list_df = [node, new_long, new_lat, new_zeta, new_w_mag, new_w_dir, new_time]
    df = pd.DataFrame({"node": list_df[0], "lon": list_df[1], "lat": list_df[2], "max_ele": list_df[3], "swan_HS_max": list_df[4], "swan_DIR_max": list_df[5], "time_max_ele": list_df[6]})

    if isinstance(N, unicode) and isinstance(S, unicode) and isinstance(E, unicode) and isinstance(W, unicode):
	N = float(N)
    	S = float(S)
    	E = float(E)
    	W = float(W)

    	if (E<=180) and (W>=-180) and (N<=90) and (S>=-90):
    		arcpy.AddMessage("Valid coodinates...")
    		df = df.loc[(df['lon']<E) & (df['lon']>W) & (df['lat']>S) & (df['lat']<N)]

    else:
    	arcpy.AddMessage("Invalid/missing coodinates, results will be saved for the entire study area...")

    # Saving the output file
    # df.save(OUTPUT_FILE)
    df.to_csv(OUTPUT_FILE,index=False)

    # Elapse time and finishing script
    arcpy.AddMessage("End of Script, Process Completed Successfully!")
    #stopTime = time.clock()
    #elapTime = stopTime - startTime
    #arcpy.AddMessage("Total time to run the script: " + str(round(elapTime)) + " seconds")   


except:
    arcpy.AddMessage("Error while running script...")