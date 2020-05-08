'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: SWAN+ADCIRC PRE-PROCESSING
 
Title:  surface_directional_effective_roughness_length
 
Description: Populates the fields  <nodeID> and <value1, value2,... value12> (surface_directional_effective_roughness_length)
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
fort.13
 
Output files:
RoughLength.dbf
 
***********************************
Version history: 
Version 4
Author: Eric Ong
Created on February 12, 2015
Comments: Creation, development and testing for ArcGIS 10.2 

Future Improvements: Implement into ArcTool Box 
***********************************
'''

# Import modules

import time
import arcpy
import os
arcpy.env.overwriteOutput = True
print("Start working...")
startTime = time.clock()

try:
    def makeTable():
        txtFile = arcpy.GetParameterAsText(0)
        newTB = arcpy.GetParameterAsText(1)

        arcpy.CreateTable_management(os.path.dirname(newTB), os.path.basename(newTB),)


        #Add attribute fields to table
        arcpy.AddField_management(newTB,"NodeID","long")
        arcpy.AddField_management(newTB,"Value1","float")
        arcpy.AddField_management(newTB,"Value2","float")
        arcpy.AddField_management(newTB,"Value3","float")
        arcpy.AddField_management(newTB,"Value4","float")
        arcpy.AddField_management(newTB,"Value5","float")
        arcpy.AddField_management(newTB,"Value6","float")
        arcpy.AddField_management(newTB,"Value7","float")
        arcpy.AddField_management(newTB,"Value8","float")
        arcpy.AddField_management(newTB,"Value9","float")
        arcpy.AddField_management(newTB,"Value10","float")
        arcpy.AddField_management(newTB,"Value11","float")
        arcpy.AddField_management(newTB,"Value12","float")

        #Open the text file and read the number of nodes
        input = file(txtFile, "r")
        input.readline()
        line = input.readline()
        totalNodes=line.split() #Number of nodes
        nunnodes = int(totalNodes[0])
        line = input.readline()
        data=line.split()
        nunparameter=int(data[0]) #Number of attributes

        print('This ADCIRC GRID has: ' + str(nunnodes) + ' nodes')
        print('This Fort.13 file has: ' + str(nunparameter) + ' parameters')
        print('Importing the parameters from the Fort.13 ...')

        #Reads line until line with parameter
        count=0
        while count == 0:
            line = input.readline()
            data = line.split()
            if str(data[0]) == str("surface_directional_effective_roughness_length"):
                count=+1

        line = input.readline()
        line = input.readline()
        line = input.readline()
        data = line.split()
        defaultValue = float(data[0])

        cur = arcpy.InsertCursor(newTB)
        index=1
        for row in range (0,nunnodes):
            row = cur.newRow()
            row.NodeID = long(index)
            
            row.Value1 = defaultValue
            row.Value2 = defaultValue
            row.Value3 = defaultValue
            row.Value4 = defaultValue
            row.Value5 = defaultValue
            row.Value6 = defaultValue
            row.Value7 = defaultValue
            row.Value8 = defaultValue
            row.Value9 = defaultValue
            row.Value10 = defaultValue
            row.Value11 = defaultValue
            row.Value12 = defaultValue
            
            cur.insertRow(row)
            index=index+1       
        del cur, row

        #Adds non-default values
        count2=0
        while count2 == 0:
            line = input.readline()
            data = line.split()
            if str(data[0]) == str('surface_directional_effective_roughness_length'):
                count2=+1
                
        line = input.readline()
        totalValues = line.split()

        if int(line) > 0:
            cur2 = arcpy.UpdateCursor(newTB)
            for i in range(int(line)):
                line=input.readline()
                data=line.split()
                tmpnode = long(data[0])
                row = cur2.next()
                tmpnode2 = row.NodeID
                while tmpnode <> tmpnode2:
                    row = cur2.next()
                    tmpnode2 = row.NodeID
                row.Value1 = float(data[1])
                row.Value2 = float(data[2])
                row.Value3 = float(data[3])
                row.Value4 = float(data[4])
                row.Value5 = float(data[5])
                row.Value6 = float(data[6])
                row.Value7 = float(data[7])
                row.Value8 = float(data[8])
                row.Value9 = float(data[9])
                row.Value10 = float(data[10])
                row.Value11 = float(data[11])
                row.Value12 = float(data[12])
                
                cur2.updateRow(row)
            del row, cur2
            line = input.readline()

        arcpy.DeleteField_management(newTB, "Field1")
        input.close()
    makeTable()

    print("End of Script, Process Completed Successfully!")
    stopTime = time.clock()
    elapTime = stopTime - startTime
    print("Total time to run the script: " + str(round(elapTime)) + " seconds")

except:
    arcpy.AddMessage("Error while running script...")
