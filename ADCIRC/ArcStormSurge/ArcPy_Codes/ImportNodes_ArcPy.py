'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: SWAN+ADCIRC PRE-PROCESSING
 
Title:  ImportNodes
 
Description: Creates a point feature class and populates the fields <xcoord>, <ycoord>, <nodeID>, <bathimetry> and <elevation> 
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
fort.14
 
Output files:
MeshNodes.shp
 
***********************************
Version history:
 
Versions 1-3
Author: Celso Ferreira
Created on August, 2011
Comments:Geodatabase and Code: creation, development and testing for ArcGIS 9.3
Implementation of new Arc PY functionality and update to ArcGIS 10
 
Version 4
Author: Eric Ong
Created on January 26, 2015
Comments: Revised to update to ArcGIS 10.2
Defines coordinate system as NAD83 2011 (104145)

Future Improvements: Implement import boundary, add grid info, and projection 
*********************************** 
'''

#---------------- Import Modules

# Import modules and create the geoprocessor
import arcpy
import os
import time
import numpy
from numpy import *
arcpy.env.overwriteOutput = True

# launch Console and Start timming
arcpy.AddMessage("Start working...")
startTime = time.clock()


    # ---------------- Data INPUT

    # Create variables for the paths
txtFile = arcpy.GetParameterAsText(0)
newFC = arcpy.GetParameterAsText(1)

try:
    # ---------------- CODE

    # Create a new feature class
    # At this point I am importing a known projection - improve this in the future
    arcpy.CreateFeatureclass_management(os.path.dirname(newFC), os.path.basename(newFC), "Point", "", "", "" , "")
    arcpy.AddField_management (newFC, "NodeID", "LONG") 
    arcpy.AddField_management (newFC, "elev", "float")
    arcpy.AddField_management (newFC, "bathy", "float")

    # Create point and cursor objects
    pnt = arcpy.CreateObject("Point")
    cur = arcpy.InsertCursor(newFC)

    # Open the text file
    input = file(txtFile, "r")
    input.readline()
    line = input.readline()
    data=line.split()
    nunnodes = int(data[1])
    arcpy.AddMessage('This ADCIRC GRID has: ' + str(nunnodes) + ' nodes')
    arcpy.AddMessage('Processing the GRID...')

    # Loop through the coordinate values
    for num in range(nunnodes):
        line = input.readline()
        data=line.split()
        pnt.X = float(data[1])
        pnt.Y = float(data[2])
        pnt.Z = float(data[3])
        row = cur.newRow()
        row.shape = pnt
        row.NodeID = long(data[0])
        row.bathy = float(data[3])
        row.elev = -1 * float(data[3])
        cur.insertRow(row)

    del pnt, cur, row

    input.close()    
    SR = arcpy.SpatialReference(104145) #change coordinate system here*** 
     
    
    arcpy.DefineProjection_management(newFC, SR)              
    # Elapse time and finishing script
    arcpy.AddMessage("End of Script, Process Completed Successfully!")
    stopTime = time.clock()
    elapTime = stopTime - startTime
    arcpy.AddMessage("Total time to run the script: " + str(round(elapTime)) + " seconds")
except:
    arcpy.AddMessage("Error while running script...")
