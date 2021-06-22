######################################################
## Wave Transformation Tool
######################################################
## Author: F. Cassalho
## Version: ArcMap 10.5.X
## Inputs: Wave magnitude and wave direction rasters
## Output: Wave transformation % raster
## Date: 5/10/2021
######################################################


# Import libraries and create the geoprocessor
import arcpy
import os
import numpy as np
import time
arcpy.env.overwriteOutput = True


# launch Console and Start timming
arcpy.AddMessage("Start working...")
startTime = time.clock()



# Setting the input and output files and folders
tif_path_DIR = arcpy.GetParameterAsText(0)  # Raster file
tif_path_MAG = arcpy.GetParameterAsText(1)  # Raster file

OUTPUT_WAVE_TRANS = arcpy.GetParameterAsText(2)  # Raster file path
OUTPUT_WAVE_DIR = arcpy.GetParameterAsText(3)  # Raster file path

try:

    # Getting the attributes to ensure that the outputs will have the same coordinates and characteristics as the inputs
    arcpy.env.outputCoordinateSystem = tif_path_DIR  # The output coordinate system is the same as the input
    dsc = arcpy.Describe(tif_path_DIR)  # Getting the attributes
    sr = dsc.SpatialReference  # Getting the projection
    ext = dsc.Extent  # Getting the extent
    ll = arcpy.Point(ext.XMin,ext.YMin)  # Getting the min x and y coordinates


    tif_DIR = arcpy.Raster(tif_path_DIR)  # Opening the input as a raster
    tif_MAG = arcpy.Raster(tif_path_MAG)  # Opening the input as a raster


    wave_dir = arcpy.RasterToNumPyArray(tif_DIR)  # Opening the input raster as a numpyarray
    wave_mag = arcpy.RasterToNumPyArray(tif_MAG)  # Opening the input raster as a numpyarray



    ############################ Here is the code that process the inputs ############################
    class_dir = []
    class_neighbor = []
    class_element = []
    class_hs = []

    for i in range(len(wave_dir)):
        i_dir = []
        i_neighbor = []
        i_element = []
        i_hs = []
        
        for j in range(len(wave_dir[i])):
            element_dir = -99
            neighbor = -99
            element = wave_dir[i][j]
            hs = wave_mag[i][j]

            
            if ((element >= 332.5) and (element < 360)) or ((element >= 0) and (element < 22.5)):
                element_dir = 1
                if (i != 0):            
                    neighbor = wave_mag[i-1][j]           
            
            elif (element >= 22.5) and (element < 67.5):
                element_dir = 2
                if (i != 0) and (j != len(wave_dir[i])-1):
                    neighbor = wave_mag[i-1][j+1]
            
            elif (element >= 67.5) and (element < 112.5):
                element_dir = 3  
                if (j != len(wave_dir[i])-1): 
                    neighbor = wave_mag[i][j+1]
            
            elif (element >= 112.5) and (element < 157.5):
                element_dir = 4
                if (i != len(wave_dir)-1) and (j != len(wave_dir[i])-1):
                    neighbor = wave_mag[i+1][j+1]
            
            elif (element >= 157.5) and (element < 202.5):
                element_dir = 5   
                if (i != len(wave_dir)-1):
                    neighbor = wave_mag[i+1][j]
            
            elif (element >= 202.5) and (element < 247.5):
                element_dir = 6
                if (i != len(wave_mag)-1) and (j != 0):
                    neighbor = wave_mag[i+1][j-1]
            
            elif (element >= 247.5) and (element < 292.5):
                element_dir = 7   
                if (j != 0):
                    neighbor = wave_mag[i][j-1]
            
            elif (element >= 292.5) and (element < 332.5):
                element_dir = 8
                if (i != 0) and (j != 0):
                    neighbor = wave_mag[i-1][j-1]
            
            else:
                element_dir = -99
                neighbor = -99

            i_dir.append(element_dir)
            i_neighbor.append(neighbor)
            i_element.append(element)
            i_hs.append(hs)
        class_dir.append(i_dir)
        class_neighbor.append(i_neighbor)
        class_element.append(i_element)
        class_hs.append(i_hs)
    ##################################################################################################


    ###################### Here is the code that calculates wave transformation ######################
    arr_neighbor = np.array(class_neighbor, dtype=np.float32)
    arr_dir = np.array(class_dir, dtype=np.float32)
    arr_hs = np.array(class_hs, dtype=np.float32)
    arr_hs = np.where((arr_hs < 0), 0, arr_hs)
    arr_neighbor = np.where((arr_neighbor < 0), 1, arr_neighbor)
    att = np.divide(arr_hs, arr_neighbor)
    # att = np.divide(arr_neighbor, arr_hs)
    att = np.where((att <= -0), 1, att)
    att_percent = (att-1)*100 #this is percentage wave transformation
    ##################################################################################################


    # Creating the output raster with the same attributes of the inputs
    wave_trans_raster = arcpy.NumPyArrayToRaster(att_percent, ll, dsc.meanCellWidth, dsc.meanCellHeight)
    wave_dir_raster = arcpy.NumPyArrayToRaster(arr_dir, ll, dsc.meanCellWidth, dsc.meanCellHeight)
    arcpy.DefineProjection_management(wave_trans_raster, sr)
    arcpy.DefineProjection_management(wave_dir_raster, sr)


    # Savingthe output rasters 
    wave_trans_raster.save(OUTPUT_WAVE_TRANS)
    wave_dir_raster.save(OUTPUT_WAVE_DIR)
	

    # Elapse time and finishing script
    arcpy.AddMessage("End of Script, Process Completed Successfully!")
    stopTime = time.clock()
    elapTime = stopTime - startTime
    arcpy.AddMessage("Total time to run the script: " + str(round(elapTime)) + " seconds")

except:
    arcpy.AddMessage("Error while running script...")