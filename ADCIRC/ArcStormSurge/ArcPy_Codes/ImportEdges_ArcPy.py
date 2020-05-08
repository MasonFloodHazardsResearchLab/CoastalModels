'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: SWAN+ADCIRC PRE-PROCESSING
 
Title:  ImportEdges
 
Description: Creates a line feature class and populates the <FromNodeID>, <ToNodeID>, and <Size> 
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
fort.14
 
Output files:
MeshEdges.shp
 
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

Future Improvements: Implement import boundary, add grid info, and projection 
*********************************** 
'''

# ---------------- Import Modules

# Import modules and create the geoprocessor
import arcpy
import os
import time
import numpy
from numpy import *
arcpy.env.overwriteOutput = True


arcpy.AddMessage("Start working...")
arcpy.AddMessage("Warning: Depending on the number of edges in the FE Grid, this operation might take a long time...")
startTime = time.clock()

# ---------------- Data INPUT

# Create variables for the paths - IDE
txtFile = arcpy.GetParameterAsText(0)
newFC = arcpy.GetParameterAsText(1)    
try: 
    # ---------------- CODE
    # Create a new feature class
    # At this point I am importing a known projection - improve this in the future
    arcpy.CreateFeatureclass_management(os.path.dirname(newFC), os.path.basename(newFC), "Polyline", "", "", "" , "") # "r"F:\research\research_CMP\ADCIRC_codes\python\adcirc_grid_manning_projected2.shp")
    arcpy.AddField_management (newFC, "MeshID", "LONG") 
    arcpy.AddField_management (newFC, "numele", "LONG")     
    arcpy.AddField_management (newFC, "Node1", "LONG")
    arcpy.AddField_management (newFC, "Node2", "LONG")
    arcpy.AddField_management (newFC, "Node3", "LONG")

    # Describe the new feature class
    desc = arcpy.Describe(newFC)
    shpFld = desc.ShapeFieldName

    # Create point and cursor objects
    lineArray = arcpy.CreateObject("Array")
    pnt = arcpy.CreateObject("Point")
    cur = arcpy.InsertCursor(newFC)
    array = arcpy.CreateObject("Array")
    pnt = arcpy.CreateObject("Point")

    # Open the text file
    input = file(txtFile, "r")

    input.readline()
    line = input.readline()
    data=line.split()
    #print data
    nunnodes = int(data[1])
    nunedges = int(data[0])
    #nunnodes2 = 3
    arcpy.AddMessage('This ADCIRC GRID has: ' + str(nunedges) + ' edges')
    arcpy.AddMessage('Processing the GRID...')

    coord = zeros((nunnodes, 2))
    arcpy.AddMessage('Reading the coordinates of the nodes...')
    # Read the coordinates of the nodes and create array
    for num in range(nunnodes):
        line = input.readline()
        data = line.split()
        coord[num,0] = float(data[1])
        coord[num,1] = float(data[2])

    # Loop and read the edges    
    arcpy.AddMessage('Creating the edges...')
    for num in range(nunedges):
        line = input.readline()
        data=line.split()
        temp1 = int(data[2])-1
        temp2 = int(data[3])-1
        temp3 = int(data[4])-1
        # First node 
        pnt.X = float(coord[temp1,0])
        pnt.Y = float(coord[temp1,1])
        array.add(pnt)
        # Second node 
        pnt.X = float(coord[temp2,0])
        pnt.Y = float(coord[temp2,1])
        array.add(pnt)
        # Third node 
        pnt.X = float(coord[temp3,0])
        pnt.Y = float(coord[temp3,1])
        array.add(pnt)
        # First node  - close the polygon
        pnt.X = float(coord[temp1,0])
        pnt.Y = float(coord[temp1,1])
        array.add(pnt)

        row = cur.newRow()
        row.shape = array
        #row.rowid = long(data[0])
        row.MeshID = long(data[0])
        row.numele = int(data[1])
        row.Node1 = long(data[2])
        row.Node2 = long(data[3])
        row.Node3 = long(data[4])
        cur.insertRow(row)
        array.removeAll()

    del lineArray, pnt, cur, row, array

    input.close() 
                
    # Elapse time and finishing script
    arcpy.AddMessage("End of Script, Process Completed Successfully!")
    stopTime = time.clock()
    elapTime = stopTime - startTime
    arcpy.AddMessage("Total time to run the script: " + str(round(elapTime)) + " seconds")
except:
    arcpy.AddMessage("Error while running script...")
