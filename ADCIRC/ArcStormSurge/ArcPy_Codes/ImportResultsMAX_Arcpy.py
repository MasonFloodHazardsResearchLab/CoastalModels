'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: POST-PROCESSING
 
Title:  ImportResultsMAX
 
Description: Import results for MAXELE for every node and create a table
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
maxele.63
 
Output files:
ResultsMax table
 
***********************************
Version history:
 
Versions 1-3
Author: Celso Ferreira
Created on January 27, 2011
Comments:Geodatabase and Code: creation, development and testing for ArcGIS 9.3
Implementation of new Arc PY functionality and update to ArcGIS 10
 
Version 4
Author: Eric Ong
Created on April 2, 2015
Comments: Revised anf updated to ArcPy 10.2

Future Improvements:  
*********************************** 
'''

# Import modules and create the geoprocessor
import arcpy
import os
import time

arcpy.env.overwriteOutput = True

arcpy.AddMessage("Start working...")
# Create variables for the paths
startTime = time.clock()
txtFile = arcpy.GetParameterAsText(0)
newTB = arcpy.GetParameterAsText(1)

try:
    
    # Create Max table

    arcpy.CreateTable_management(os.path.dirname(newTB), os.path.basename(newTB),)

    #Process: Add attribute fields to table
    arcpy.AddField_management(newTB,"node","long")
    arcpy.AddField_management(newTB,"result","double", "20", "20")


    #vtab = arcpy.CreateObject("ValueTable",2)


    # Open the text file and read the number of nodes
    input = file(txtFile, "r")
    input.readline()
    line = input.readline()
    data=line.split()
    nunnodes = int(data[1])
    line = input.readline()

    arcpy.AddMessage( 'This ADCIRC MAX Result File has: ' + str(nunnodes) + ' nodes')
    arcpy.AddMessage( 'Importing ADCIRC results values to Table ...')

    cur = arcpy.InsertCursor(newTB)

    for row in range (0,nunnodes):
        
        line=input.readline()
        if not line: break
        
        data=line.split()    
        row = cur.newRow()
        row.node = long(data[0])
        result = float(data[1])
        if result == -99999:
            row.result = 0
        else:
            row.result = float(data[1])
        cur.insertRow(row)

    del cur, row


    input.close()     


    # Elapse time and finishing script
    arcpy.AddMessage("End of Script, Process Completed Successfully!")
    stopTime = time.clock()
    elapTime = stopTime - startTime
    arcpy.AddMessage("Total time to run the script: " + str(round(elapTime)) + " seconds")
except:
    arcpy.AddMessage("Error while running script...")
