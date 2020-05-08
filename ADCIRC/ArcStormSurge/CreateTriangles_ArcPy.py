'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: SWAN+ADCIRC PRE-PROCESSING
 
Title:  CreateElements
 
Description: Creates a polygon feature class and populates the
<Node1>, <Node2>, <Node3> (<NodeID> values of the nodes that form each element), <ElementID> and <Area> 
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
MeshEdges.shp
 
Output files:
MeshElements.shp
 
***********************************
Version history: 
Version 4
Author: Eric Ong
Created on December 17, 2014
Comments: Creation, development and testing for ArcGIS 10.2. Does not have Node1, Node2, Node3 attributes.
Defines coordinate system as NAD83 2011 (104145)

Future Improvements: Implement import boundary, add grid info. Add missing attributes 
***********************************
'''

# Import arcpy module
import arcpy
import time

arcpy.env.overwriteOutput = True

# launch Console and Start timming
arcpy.AddMessage("Start working...")
startTime = time.clock()

# Local variables:  (Must change file path)
MeshEdges_shp = arcpy.GetParameterAsText(1)
txtFile = arcpy.GetParameterAsText(0)

MeshElements_shp = arcpy.GetParameterAsText(2)

try:
    # Process: Feature To Polygon  (Must change file path)
    arcpy.FeatureToPolygon_management(MeshEdges_shp, MeshElements_shp, "", "ATTRIBUTES", "")

    arcpy.AddField_management (MeshElements_shp, "Node1", "LONG")
    arcpy.AddField_management (MeshElements_shp, "Node2", "LONG")
    arcpy.AddField_management (MeshElements_shp, "Node3", "LONG")

    cur = arcpy.InsertCursor(MeshElements_shp)
    array = arcpy.CreateObject("Array")


    arcpy.AddMessage("Reading file...")
    input = file(txtFile, "r")
    input.readline()
    line = input.readline()
    data=line.split()
    #print data
    nunnodes = int(data[1])
    nunedges = int(data[0])
    print(nunedges)
    for num in range(nunnodes):
        line = input.readline()

    for num in range(0, nunedges):
        line = input.readline()
        data=line.split()
        #print(data[2])
        row = cur.newRow()
        row.Node1 = long(data[2])
        row.Node2 = long(data[3])
        row.Node3 = long(data[4])

        cur.insertRow(row)
        
                         
    del cur, row



    input.close()
    SR = arcpy.SpatialReference(104145) #change coordinate system here*** 
     
    
    arcpy.DefineProjection_management(MeshElements_shp, SR)
    # Elapse time and finishing script
    arcpy.AddMessage("End of Script, Process Completed Successfully!")
    stopTime = time.clock()
    elapTime = stopTime - startTime
    arcpy.AddMessage("Total time to run the script: " + str(round(elapTime)) + " seconds")
except:
    arcpy.AddMessage("Error while running script...")
