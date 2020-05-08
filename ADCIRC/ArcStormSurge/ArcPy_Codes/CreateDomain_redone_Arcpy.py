'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: SWAN+ADCIRC PRE-PROCESSING
 
Title:  CreateDomain
 
Description: Creates a polygon feature class based on the mesh spatial domain
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
AllBoundaries.shp

 
Output files:
DomainFill.shp
Land.shp
Boundary.shp
 
***********************************
Version history: 
Version 4
Author: Eric Ong
Created on December 17, 2014
Comments: Creation, development and testing for ArcGIS 10.2
Defines coordinate system as NAD83 2011 (104145)

Future Improvements: Implement import boundary, grid info, and implement the fort.14 as input instead of shapefile. 
***********************************
'''

# Import arcpy module
import arcpy
import time

arcpy.env.overwriteOutput = True

# launch Console and Start timming
arcpy.AddMessage("Start working...")
startTime = time.clock()

# Local variables:
inputFC = arcpy.GetParameterAsText(0)

Boundary = arcpy.GetParameterAsText(1)
Land = arcpy.GetParameterAsText(2)
outputFC = arcpy.GetParameterAsText(3)

userIbtype1 = arcpy.GetParameterAsText(4)
userIbtype2 = arcpy.GetParameterAsText(5)

#elevationBoundary = arcpy.GetParameterAsText(4)
#externalBoundary = arcpy.GetParameterAsText(5)


elevationBoundary = '\"IBTYPE\" = ' + str(userIbtype1)
externalBoundary = '\"IBTYPE\" = ' + str(userIbtype2)

try:

    arcpy.Select_analysis(inputFC, Boundary, elevationBoundary)
    arcpy.Select_analysis(inputFC, Land, externalBoundary)

    arcpy.FeatureToPolygon_management([Boundary,Land],outputFC,"", "ATTRIBUTES","")



    SR = arcpy.SpatialReference(104145) #change coordinate system here*** 
     
    
    arcpy.DefineProjection_management(outputFC, SR)

	

except:
    arcpy.AddMessage("Error while running script...")
   


# Elapse time and finishing script
arcpy.AddMessage("End of Script, Process Completed Successfully!")
stopTime = time.clock()
elapTime = stopTime - startTime
arcpy.AddMessage("Total time to run the script: " + str(round(elapTime)) + " seconds")





