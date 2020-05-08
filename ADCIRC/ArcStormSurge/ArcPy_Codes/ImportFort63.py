'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: POST-PROCESSING
 
Title:  ImportFort63
 
Description: populates the <ws>, <date> and <nodeID> fields
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
fort.63
 
Output files:
wl_fort63_test.dbf
 
***********************************
Version history:
 
Versions 1-3
Author: Celso Ferreira
Created on August 18, 2010
Comments:Geodatabase and Code: creation, development and testing for ArcGIS 9.3
Implementation of new Arc PY functionality and update to ArcGIS 10
 
Version 4
Author: Eric Ong
Created on April 2, 2015
Comments: Table only generates the first time step

Future Improvements: Be able to specify time step and include those time steps in table  
*********************************** 
'''

# Import modules and create the geoprocessor
import arcpy
import os
import time
from arcpy import env

arcpy.env.overwriteOutput = True


# launch Console and Start timming
print "Start working..."
startTime = time.clock()


# Create variables for the paths

txtFile = arcpy.GetParameterAsText(0)
newTB = arcpy.GetParameterAsText(1)




# Create TS table
print"Creating table in ArcStormSurge Geodatabase"
# Process: Create the empty table
arcpy.CreateTable_management(os.path.dirname(newTB), os.path.basename(newTB),)

# Process: Add attribute fields to table
arcpy.AddField_management(newTB,"node","long")
arcpy.AddField_management(newTB,"wl","float")
arcpy.AddField_management(newTB,"input_time", "text")
arcpy.AddField_management(newTB,"time", "date")
# Describe the new feature class


# Create point and cursor objects
cur = arcpy.InsertCursor(newTB)


# Open the text file
input = file(txtFile, "r")

print 'Reading the 63 File'
# Loop through the coordinate values

input.readline()
line = input.readline()
data=line.split()
nodes = long(data[1])
###
time_step = long(data[0])
###
row = cur.newRow()

print(nodes)

for i in range(1,2):
    try:
        line = input.readline()
        data=line.split()
        readtime = str(data[0])
        for rows in range(nodes):
            line = input.readline()
            data=line.split()
            row.node = long(data[0])
            row.wl = float(data[1])
            row.input_time = readtime
            cur.insertRow(row)
            row = cur.newRow()
    except:
        break
    
print(line)
'''
    try:
        for j in range(1,num_time_step):
            for j in range(1,nodes):
                line = input.readline()
        
'''    
arcpy.ConvertTimeField_management(newTB, "input_time", "s", "time")

del cur, row
#
input.close() 

# Elapse time and finishing script
print "End of Script, Process Completed Successfully!"
stopTime = time.clock()
elapTime = stopTime - startTime
print "Total time to run the script: " + str(round(elapTime)) + " seconds"

















