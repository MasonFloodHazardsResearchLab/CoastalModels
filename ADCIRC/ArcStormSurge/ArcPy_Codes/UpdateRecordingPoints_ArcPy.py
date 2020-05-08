'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: SWAN+ADCIRC PRE-PROCESSING
 
Title:  UpdateRecordingPoints
 
Description: Updates an existing fort.15
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
fort.15
MonitoringStations.shp
 
Output files:
updatedFort.15
 
***********************************
Version history:
 
Versions 1-3
Author: Celso Ferreira
Created on August 18, 2010
Comments:Geodatabase and Code: creation, development and testing for ArcGIS 9.3
Implementation of new Arc PY functionality and update to ArcGIS 10
 
Version 4
Author: Eric Ong
Created on March 4, 2015
Comments: Revised and updated to ArcGIS 10.2

Future Improvements: Does not work properly, rewriting may include duplicates from previous fort.15
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

# ---------------- Data INPUT

# Create variables for the paths - IDE
txtFile = arcpy.GetParameterAsText(0)
txtFile2 = arcpy.GetParameterAsText(2)

pnt1 = arcpy.GetParameterAsText(1) 
 

try:
    # ---------------- CODE

    #add index 
    index =0

    input = file(txtFile, "r")
    output = file(txtFile2, "w")


    # counting stations
    cur = arcpy.SearchCursor(pnt1)
    row = cur.next()

    while row:
        row = cur.next()  
        index=index+1       
            

    del cur, row             

    x=1
    while x==1:


        line = input.readline()
        
        if not line: break
        output.write(line)
        data=line.split()
        for word in data:
            if word == "ANGINN":
                x=2

    line = input.readline()
    output.write(line)

    line = input.readline()
    data=line.split()


    output.write(str(index)+"                 ! TOTAL NUMBER OF ELEVATION RECORDING STATIONS"+"\n")



    # start writing here

    cur = arcpy.SearchCursor(pnt1)
    row = cur.next()
    index=1
    while row:
        output.write(str(row.Lat).ljust(15, "0")+" "+(str(row.Long).ljust(14, "0")+"  "+str(row.name)+"  "+"\n"))
        row = cur.next()  
        index=index+1       
            

    del cur, row             

    for i in range(index-1):
        input.readline()
    while 1:

        line = input.readline()
        
        if not line: break 
        output.write(line)

    print(index)
    output.close()
    input.close()


    # Elapse time and finishing script
    parcpy.AddMessage("End of Script, Process Completed Successfully!")
    stopTime = time.clock()
    elapTime = stopTime - startTime
    arcpy.AddMessage("Total time to run the script: ") + str(round(elapTime)) + " seconds"
except:
    arcpy.AddMessage("Error while running script...")
