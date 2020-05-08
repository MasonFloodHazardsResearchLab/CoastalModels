'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: POST-PROCESSING
 
Title:  HurricaneEyePath
 
Description: creates a point feature class and populates  the <stormID>, <date>, <forwardSpeed> and <centralPressure> attributes
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
fort.22
 
Output files:
HurricaneEyePath.shp
 
***********************************
Version history: 
Version 4
Author: Eric Ong
Created on February 13, 2015
Comments: Creation, development and testing for ArcGIS 10.2 
Defines coordinate system as NAD83 2011 (104145)

Future Improvements: 
***********************************
'''

# Import modules
import time
import arcpy
import os
arcpy.env.overwriteOutput = True
arcpy.AddMessage("Start working...")
startTime = time.clock()

# Change file paths
txtFile = arcpy.GetParameterAsText(0)
newFC = arcpy.GetParameterAsText(1)
newFC2 = arcpy.GetParameterAsText(2)

try:
    # Create feature class
    arcpy.CreateFeatureclass_management(os.path.dirname(newFC), os.path.basename(newFC), "Point", "", "", "" , "")
    # Add fields to table
    arcpy.AddField_management(newFC,"BASIN","text")
    arcpy.AddField_management(newFC,"CycloneNum","short")
    arcpy.AddField_management(newFC,"YYYYMMDDHH","text")
    arcpy.AddField_management(newFC,"OTSNumber","text")
    arcpy.AddField_management(newFC,"Acronym","text")
    arcpy.AddField_management(newFC,"Forecast","short")
    arcpy.AddField_management(newFC,"LatOfEye","text")
    arcpy.AddField_management(newFC,"LongOfEye","text")
    arcpy.AddField_management(newFC,"MaxWind","short")
    arcpy.AddField_management(newFC,"MinSeaMB","short")
    arcpy.AddField_management(newFC,"CycloneLVL","text")
    arcpy.AddField_management(newFC,"WindIntens","short")
    arcpy.AddField_management(newFC,"RadiusCode","text")
    arcpy.AddField_management(newFC,"WindQuad1","short")
    arcpy.AddField_management(newFC,"WindQuad2","short")
    arcpy.AddField_management(newFC,"WindQuad3","short")
    arcpy.AddField_management(newFC,"WindQuad4","short")
    arcpy.AddField_management(newFC,"BGPressure","short")
    arcpy.AddField_management(newFC,"Isobar","text")
    arcpy.AddField_management(newFC,"Rmax","short")
    arcpy.AddField_management(newFC,"Gusts","text")
    arcpy.AddField_management(newFC,"EyeDia","text")
    arcpy.AddField_management(newFC,"SubregCode","text")
    arcpy.AddField_management(newFC,"MaxSeas","text")
    arcpy.AddField_management(newFC,"Forecaster","text")
    arcpy.AddField_management(newFC,"Direction","short")
    arcpy.AddField_management(newFC,"StormSpeed","short")
    arcpy.AddField_management(newFC,"Name","text")
    arcpy.AddField_management(newFC,"TimeRecord","text")
    arcpy.AddField_management(newFC,"Isotachs","short")
    arcpy.AddField_management(newFC,"Radii1","short")
    arcpy.AddField_management(newFC,"Radii2","short")
    arcpy.AddField_management(newFC,"Radii3","short")
    arcpy.AddField_management(newFC,"Radii4","short")
    arcpy.AddField_management(newFC,"RmaxQuad1","float")
    arcpy.AddField_management(newFC,"RmaxQuad2","float")
    arcpy.AddField_management(newFC,"RmaxQuad3","float")
    arcpy.AddField_management(newFC,"RmaxQuad4","float")
    arcpy.AddField_management(newFC,"HollandB","double")

    cur = arcpy.InsertCursor(newFC)
    pnt = arcpy.CreateObject("Point")
    row = cur.newRow()

    fort22 = open(txtFile, "r")
    arcpy.AddMessage("Reading Fort.22...")

    for line in fort22:
        #print(line)
        #line = fort22.readline()
        data = line.split(",")
        #print(data)
        
        xCoorTxt = data[6]
        #print(xCoorTxt)

        ###
        xCoorInt = float(xCoorTxt[:-1])
        xCoorIntEdit = (xCoorInt/10)
        
        yCoorTxt = data[7]
        yCoorInt = float(yCoorTxt[:-1])
        yCoorIntEdit = (yCoorInt/10)
        ###
        
        
        if "W" in yCoorTxt:
            #print("true")
            yCoorIntEdit = (yCoorIntEdit * -1)

        if "S" in xCoorTxt:
            #print("true")
            xCoorIntEdit = (xCoorIntEdit * -1)
        ###

        #print(yCoorIntEdit)
        pnt.X = yCoorIntEdit
        pnt.Y = xCoorIntEdit
        
        row = cur.newRow()
        row.shape = pnt
        
        row.BASIN = str(data[0])
        row.CycloneNum = int(data[1])
        row.YYYYMMDDHH = str(data[2])
        row.OTSNumber = str(data[3])
        row.Acronym = str(data[4])
        row.Forecast = int(data[5])
        row.LatOfEye = str(data[6])
        row.LongOfEye = str(data[7])
        row.MaxWind = int(data[8])
        row.MinSeaMB = int(data[9])
        row.CycloneLVL = str(data[10])
        row.WindIntens = int(data[11])
        row.RadiusCode = str(data[12])
        row.WindQuad1 = int(data[13])
        row.WindQuad2 = int(data[14])
        row.WindQuad3 = int(data[15])
        row.WindQuad4 = int(data[16])
        row.BGPressure = int(data[17])
        row.Isobar = str(data[18])
        row.Rmax = int(data[19])
        row.Gusts = str(data[20])
        row.EyeDia = str(data[21])
        row.SubregCode = str(data[22])
        row.MaxSeas = str(data[23])
        row.Forecaster = str(data[24])
        row.Direction = int(data[25])
        row.StormSpeed = int(data[26])
        row.Name = str(data[27])
        row.TimeRecord = str(data[28])
        row.Isotachs = int(data[29])
        row.Radii1 = int(data[30])
        row.Radii2 = int(data[31])
        row.Radii3 = int(data[32])
        row.Radii4 = int(data[33])
        row.RmaxQuad1 = float(data[34])
        row.RmaxQuad2 = float(data[35])
        row.RmaxQuad3 = float(data[36])
        row.RmaxQuad4 = float(data[37])
        row.HollandB = float(data[38])

        
        cur.insertRow(row)
    del cur, row, pnt

    fort22.close()


    arcpy.PointsToLine_management(newFC, newFC2, "", "")
    
    #srtext = arcpy.GetParameterAsText(3)
   
    SR = arcpy.SpatialReference(104145) #change coordinate system here*** 
     
    
    arcpy.DefineProjection_management(newFC, SR)
    arcpy.DefineProjection_management(newFC2, SR)


    arcpy.AddMessage("End of Script, Process Completed Successfully!")
    stopTime = time.clock()
    elapTime = stopTime - startTime
    arcpy.AddMessage("Total time to run the script: " + str(round(elapTime)) + " seconds")

except:
    arcpy.AddMessage("Error while running script...")
    
