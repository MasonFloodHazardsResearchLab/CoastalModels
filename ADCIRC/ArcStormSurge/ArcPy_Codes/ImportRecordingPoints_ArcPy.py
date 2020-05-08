'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: SWAN+ADCIRC PRE-PROCESSING
 
Title:  ImportRecordingPoints
 
Description: Creates a point feature class and populates the  attributes <pointID>, <description>, <xcoord> and <ycoord>
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
fort.15
 
Output files:
MonitoringStations.shp
 
***********************************
Version history:
 
Versions 1-3
Author: Celso Ferreira
Created August 2011
Comments:Geodatabase and Code: creation, development and testing for ArcGIS 9.3
Implementation of new Arc PY functionality and update to ArcGIS 10
 
Version 4
Author: Eric Ong
Created on March 4, 2015
Comments: Revised and updated to ArcGIS 10.2
Defines coordinate system as NAD83 2011 (104145)

Future Improvements: Implement import boundary, add grid info 
*********************************** 
'''

# Import modules 
import arcpy
import os
import time

arcpy.env.overwriteOutput = True


# launch Console and Start timming
arcpy.AddMessage("Start working...")
startTime = time.clock()


# Create variables for the paths
txtFile = arcpy.GetParameterAsText(0)
newFC = arcpy.GetParameterAsText(1)

try:
    arcpy.CreateFeatureclass_management(os.path.dirname(newFC), os.path.basename(newFC), "Point", "", "", "" , "")
    arcpy.AddField_management (newFC, "number", "LONG") 
    arcpy.AddField_management (newFC, "name", "TEXT")
    arcpy.AddField_management (newFC, "Lat", "FLOAT")
    arcpy.AddField_management (newFC, "Long", "FLOAT")
    # Describe the new feature class

    desc = arcpy.Describe(newFC)
    shpFld = desc.ShapeFieldName

    # Create point and cursor objects
    lineArray = arcpy.CreateObject("Array")
    pnt = arcpy.CreateObject("Point")
    cur = arcpy.InsertCursor(newFC)


    # Open the text file
    input = file(txtFile, "r")

    while 1:


        line = input.readline()
        if not line: break
        data=line.split()
        #print data
        
        for words in data:
            #print words
            if words == 'NOUTE,TOUTSE,TOUTFE,NSPOOLE:ELEV':
                line = input.readline()
                data=line.split()
                nummonit = long(data[0])
                print 'This control file has: ' + str(nummonit) + ' monitoring points'
                print 'Creating the ShapeFile...'
                # Loop through the coordinate values
                index=1
                for num in range(nummonit):
                   row = cur.newRow()
                   line = input.readline()
                   data=line.split()
                   pnt.X = float(data[0])
                   pnt.Y = float(data[1])
                   pnt.ID = index
                   row.shape = pnt
                   row.number = index
                   row.name = data[2]
                   row.Lat = data[1]
                   row.Long = data[0]
                   cur.insertRow(row)
                   index=index+1
                
                del  lineArray, pnt, cur, row

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



