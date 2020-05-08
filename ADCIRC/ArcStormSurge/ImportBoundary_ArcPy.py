'''
Arc StormSurge
Integrating Hurricane Storm Surge Modeling and GIS
 
--------------------------
Citation:
Ferreira, Celso M., Francisco Olivera, and Jennifer L. Irish, 2014. Arc StormSurge: Integrating Hurricane Storm Surge Modeling and GIS. Journal of the American Water Resources Association (JAWRA) 50(1): 219-233. DOI: 10.1111/jawr.12127
 
***********************************
 
Module: SWAN+ADCIRC PRE-PROCESSING
 
Title:  ImportBoundaryNodes
 
Description: Creates a point feature class and populates the fields <NodeID> and <Type>
 
-------------------------
 
Script Instructions: Replace the path for the file location of the input and output files
 
-------------------------
Input files:
fort.14
 
Output files:
AllBoundaries.shp
BoundaryNodes.shp
 
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
Comments: Revised to add AllBoundaries.shp and to fix BoundaryNodes.shp outputs 
Defines coordinate system as NAD83 2011 (104145)

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


# launch Console and Start timming
arcpy.AddMessage("Start working...")
try:
    arcpy.AddMessage("Warning: Depending on the number of edges in the FE Grid, this operation might take a long time...")
    startTime = time.clock()

    # ---------------- Data INPUT
    # Create variables for the paths - IDE
    txtFile = arcpy.GetParameterAsText(0)

    #lines
    newFC = arcpy.GetParameterAsText(1)

    #nodes
    newFC2 = arcpy.GetParameterAsText(2)

     
    # ---------------- CODE
    # Create a new feature class
    # At this point I am importing a known projection - improve this in the future
    arcpy.CreateFeatureclass_management(os.path.dirname(newFC2), os.path.basename(newFC2), "Point", "", "", "" , "")
    arcpy.CreateFeatureclass_management(os.path.dirname(newFC), os.path.basename(newFC), "POLYLINE", "", "", "" , "")
    arcpy.AddField_management (newFC, "segment", "LONG") 
    arcpy.AddField_management (newFC, "IBTYPE", "LONG")     
    arcpy.AddField_management (newFC, "BndType", "TEXT")



    ###Edited
    arcpy.AddField_management (newFC2, "NodeID", "LONG") 
    arcpy.AddField_management (newFC2, "IBTYPE", "LONG")     
    arcpy.AddField_management (newFC2, "BndType", "TEXT")




    # Describe the new feature class
    desc = arcpy.Describe(newFC)
    shpFld = desc.ShapeFieldName

    # Create point and cursor objects
    lineArray = arcpy.CreateObject("Array")
    pnt = arcpy.CreateObject("Point")
    cur = arcpy.InsertCursor(newFC)
    array = arcpy.CreateObject("Array")
    #pnt = arcpy.CreateObject("Point")


    #### Edited
    cur2 = arcpy.InsertCursor(newFC2) # new insert cursor assigned to the point shapefile for entering information
    counter = 0

    # Open the text file
    input = file(txtFile, "r")
    input.readline()
    counter = counter + 1
    line = input.readline() # reads second line of code to get node and edge information
    counter = counter + 1
    data=line.split() 
    nunnodes = int(data[1]) # gets the number of nodes
    nunedges = int(data[0]) # gets the number of edges
    arcpy.AddMessage('This ADCIRC GRID has: ' + str(nunedges) + ' edges')
    arcpy.AddMessage('Processing the GRID...')

    coord = zeros((nunnodes, 3)) # creates a zeros matrix with nunnodes number of rows and 2 columns all with the value of 0
    tempX = 0
    tempY = 0


    #HERE
    internalList = [1,4,5,11,21,24,25]

    arcpy.AddMessage('Reading the coordinates of the nodes...')
    # Read the coordinates of the nodes and create array
    for num in range(nunnodes):  # cycles through the number of nodes
        line = input.readline()

        counter = counter + 1
        
        data = line.split()

        # replaces values in zeros matrix
        coord[num,0] = float(data[1]) 
        coord[num,1] = float(data[2])

        ###Edited
        coord[num,2] = float(data[0]) ## gets the UID number
        

    # Loop and read the edges    
    arcpy.AddMessage('Creating the boundaries...')
    for num in range(nunedges): # reads over all edge information
        line = input.readline()
        counter = counter + 1

    # --------------- Reading the Elevation Boundary Conditions    
    # begin reading individual objects
    line = input.readline()
    counter = counter + 1
    data=line.split()
    numeleseg = int(data[0])
    line = input.readline()
    counter = counter + 1
    seg=1
    count = 0
    for num in range(numeleseg):    ## goes through loop once
        line = input.readline()
        counter = counter + 1
        data=line.split()
        numseg = int(data[0])

     
        try: 
            IBTYPEtemp = int(data[1])
        except:
            IBTYPEtemp = -1

        firstPt = 1
        for num2 in range(numseg):
            line = input.readline()
            counter = counter + 1
            data=line.split()
            node = int(data[0])-1    
            pnt.X = float(coord[node,0])
            pnt.Y = float(coord[node,1])

            
            array.add(pnt)

            #if firstPt == 1:
            #    tempX = pnt.X
            #    tempY = pnt.Y

            firstPt = firstPt + 1
            #### Edited
            row2 = cur2.newRow()
            row2.shape = pnt
    ##        row2.segment = long(seg)
    ##        seg = seg+1
            row2.IBTYPE = long(IBTYPEtemp)
            row2.BndType = "open boundary type, (At present the only allowable value for IBTYPEE is 0)."
            row2.NodeID = long((coord[node,2]))
            cur2.insertRow(row2)
            #lineArray.removeAll()

        pnt.X = float(tempX)
        pnt.Y = float(tempY)
        #array.add(pnt)


            
        row = cur.newRow()
        row.shape = array
        row.segment = long(seg)
        seg = seg+1
        row.IBTYPE = long(IBTYPEtemp)
        row.BndType = "open boundary type, (At present the only allowable value for IBTYPEE is 0)."
        cur.insertRow(row)
        array.removeAll()


    # --------------- Reading the Flux Boundary Conditions  
    line = input.readline()
    counter = counter + 1

    #print (line)

    data=line.split()
    numfluseg = int(data[0])
    arcpy.AddMessage("Number of additional boundary segments: "+str(numfluseg))
    line = input.readline()
    counter = counter + 1


    for num in range(numfluseg):    
        line = input.readline()
        counter = counter + 1
        data=line.split()
        numseg = int(data[0])
        try: 
            IBTYPEtemp = int(data[1])
        except:
            IBTYPEtemp = -9999

        firstPt = 1    
        for num2 in range(numseg):
            line = input.readline()
            counter = counter + 1
            data=line.split()
            node = int(data[0])-1    
            pnt.X = float(coord[node,0])
            pnt.Y = float(coord[node,1])


            array.add(pnt)

            if firstPt == 1:
                tempX = pnt.X
                tempY = pnt.Y
                #print (tempY)
            firstPt = firstPt + 1
            
            ####Edited
            row2 = cur2.newRow()
            row2.shape = pnt
            #row2.segment = long(seg)
            #seg = seg+1
            row2.IBTYPE = long(IBTYPEtemp)
            row2.BndType = "open boundary type, (At present the only allowable value for IBTYPEE is 0)."
            row2.NodeID = long((coord[node,2]))


            if IBTYPEtemp == 0:
                row.BndType = "external boundary with no normal flow as an essential boundary condition and no constraint on tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation and by zeroing the normal velocity in the momentum equations. This boundary condition should satisfy no normal flow in a global sense and no normal flow at each boundary node. This type of boundary represents a mainland boundary with a strong no normal flow condition and free tangential slip."
                
            elif IBTYPEtemp == 1:
                 row2.BndType = "internal boundary with no normal flow treated as an essential boundary condition and no constraint on the tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation and by zeroing the normal velocity in the momentum equations. This boundary condition should satisfy no normal flow in a global sense and no normal flow at each boundary node. This type of boundary represents an island boundary with a strong normal flow condition and free tangential slip."

            elif IBTYPEtemp == 2: 
                row2.BndType ="external boundary with non-zero normal flow as an essential boundary condition and no constraint on the tangential flow. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation and by specifying the non-zero normal velocity in the momentum equations. This boundary condition should correctly satisfy the flux balance in a global sense and the normal flux at each boundary node. This type of boundary represents a river inflow or open ocean boundary with a strong specified normal flow condition and free tangential slip. Discharges are specified either in the Model Parameter and Periodic Boundary Condition File for harmonic discharge forcing or in the Non-periodic, Normal Flux Boundary Condition File for time series discharge forcing."
            
            elif IBTYPEtemp == 3: 
                row2.BndType ="external barrier boundary with either zero or non-zero normal outflow from the domain as an essential boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation and by specifying the (zero or non-zero) normal velocity in the momentum equations. Non-zero normal flow is computed using a supercritical, free surface weir formula if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense and the normal flux at each boundary node. This type of boundary represents a mainland boundary comprised of a dike or levee with strong specified normal flow condition and free tangential slip. See External Barrier Boundary Note below for further information on exterior barrier boundaries."
            
            elif IBTYPEtemp == 4: 
                row2.BndType ="internal barrier boundary with either zero or non-zero normal flow across the barrier as an essential boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation and by specifying the normal velocity (zero or non-zero) in the momentum equations. Non-zero normal flow is compute using either subcritical or supercritical, free surface weir formula (based on the water level on both sides of the barrier) if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This type of boundary represents a dike or levee that lies inside the computational domain with a strong specified normal flow condition and free tangential slip. See Internal Barrier Boundary Note for further information on exterior barrier boundaries."
            
            elif IBTYPEtemp == 5: 
                row2.BndType ="internal barrier boundary with additional cross barrier pipes located under the crown.  Cross barrier flow is treated as an essential normal flow boundary condition which leaves/enters the domain on one side of the barrier and enters/leaves the domain on the corresponding opposite side of the barrier flow rate and direction are based on barrier height, surface water elevation on both sides of the barrier, barrier coefficient and the appropriate barrier flow formula.  In addition cross barrier pipe flow rate and direction are based on pipe crown height, surface water elevation on both sides of the barrier, pipe friction coefficient, pipe diameter and the appropriate pipe flow formula.  Free tangential slip is allowed"
            
            elif IBTYPEtemp == 10: 
                row2.BndType ="external boundary with no normal and no tangential flow as essential boundary conditions. This is applied by zeroing the normal boundary flux integral in the continuity equation and by setting the velocity = 0 rather than solving momentum equations along the boundary. This boundary condition should satisfy no normal flow in a global sense and zero velocity at each boundary node. This type of boundary represents a mainland boundary with strong no normal flow and no tangential slip conditions."
            
            elif IBTYPEtemp == 11: 
                row2.BndType ="internal boundary with no normal and no tangential flow as essential boundary conditions. This is applied by zeroing the normal boundary flux integral in the continuity equation and by setting the velocity = 0 rather than solving momentum equations along the boundary. This boundary condition should correctly satisfy no normal flow in a global sense and zero velocity at each boundary node. This type of boundary represents an island boundary with strong no normal flow and no tangential slip conditions."
            
            elif IBTYPEtemp == 12: 
                row2.BndType ="external boundary with non-zero normal and zero tangential flow as an essential boundary condition. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation and by setting the non-zero normal velocity and zero tangential velocity rather than solving momentum equations along the boundary. This boundary condition should correctly satisfy the flux balance in a global sense and the specified normal/zero tangential velocity at each boundary node. This type of boundary represents a river inflow or open ocean boundary in which strong normal flow is specified with no tangential slip. Discharges are specified either in the Model Parameter and Periodic Boundary Condition File for harmonic forcing or in the Non-periodic, Normal Flux Boundary Condition File for time series forcing."
            
            elif IBTYPEtemp == 13: 
                row2.BndType ="external barrier boundary with either zero or non-zero normal outflow from the domain and zero tangential flow as essential boundary conditions. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation and by setting the (zero or non-zero) normal velocity and zero tangential velocity rather than solving momentum equations along the boundary. Non-zero normal flow is computed using a supercritical, free surface weir formula if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense and the normal velocity/zero tangential velocity at each boundary node. This type of boundary represents a mainland boundary comprised of a dike or levee with strong specified normal flow and no tangential slip conditions. See External Barrier Boundary Note below for further information on exterior barrier boundaries."
            
            elif IBTYPEtemp == 20: 
                row2.BndType ="external boundary with no normal flow as a natural boundary condition and no constraint on tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) applied in the momentum equations. This boundary condition should satisfy no normal flow in a global sense, but will only satisfy no normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a mainland boundary with a weak no normal flow condition and free tangential slip."
            
            elif IBTYPEtemp == 21:
                 row2.BndType ="internal boundary with no normal flow as a natural boundary condition and no constraint on the tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. This boundary condition should satisfy no normal flow in a global sense but will only satisfy no normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents an island boundary with a weak no normal flow condition and free tangential slip."
            
            elif IBTYPEtemp == 22:
                 row2.BndType ="external boundary with non-zero normal flow as a natural boundary condition and no constraint on the tangential flow. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a river inflow or open ocean boundary with a weak specified normal flow condition and free tangential slip. Discharges are specified either in the Model Parameter and Periodic Boundary Condition File for harmonic discharge forcing or in the Non-periodic, Normal Flux Boundary Condition File for time series discharge forcing."
            
            elif IBTYPEtemp == 23:
                 row2.BndType ="external barrier boundary with either zero or non-zero normal outflow from the domain as a natural boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. Non-zero normal flow is computed using a supercritical, free surface weir formula if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a mainland boundary comprised of a dike or levee with a weak specified normal flow condition and free tangential slip. See External Barrier Boundary Note below for further information on exterior barrier boundaries."
            
            elif IBTYPEtemp == 24:
                 row2.BndType ="internal barrier boundary with either zero or non-zero normal flow across the barrier as a natural boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. Non-zero normal flow is compute using either subcritical or supercritical, free surface weir formula (based on the water level on both sides of the barrier) if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a dike or levee that lies inside the computational domain with a weak specified normal flow condition and free tangential slip. See Internal Barrier Boundary Note below for further information on exterior barrier boundaries."
            
            elif IBTYPEtemp == 25:
                 row2.BndType ="internal barrier boundary with additional cross barrier pipes located under the crown.  Cross barrier flow is treated as a natural normal flow boundary condition which leaves/enters the domain on one side of the barrier and enters/leaves the domain on the corresponding opposite side of the barrier.  Flow rate and direction are based on barrier height, surface water elevation on both sides of the barrier, barrier coefficient and the appropriate barrier flow formula.  In addition cross barrier pipe flow rate and direction are based on pipe crown height, surface water elevation on both sides of the barrier, pipe friction coefficient, pipe diameter and the appropriate pipe flow formula.  Free tangential slip is allowed."
            
            elif IBTYPEtemp == 30:
                 row2.BndType ="wave radiation normal to the boundary as a natural boundary condition. This is applied by specifying the contribution to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. The normal flow is computed using a Sommerfield radiation condition. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents an open boundary where waves are allowed to propagate freely out of the domain."
            
            elif IBTYPEtemp == 32:
                 row2.BndType ="a combined specified normal flux and outward radiating boundary.  The GWCE is forced with the total normal flux computed by adding the specified normal flux and the flux associated with the outward radiating wave. The latter is determine from a Sommerfeld type condition, flux=celerity*wave elevation. The momentum equations are used to compute the velocity field the same as for a nonboundary node."
            
            elif IBTYPEtemp == 40:
                 row2.BndType ="a zero normal velocity gradient boundary. The GWCE is forced with normal flux, the momentum eqs are sacrificed in favor of setting the velocity at a boundary node equal to the value at a fictitious point inside the domain. The fictitious point lies on the inward directed normal to the boundary a distance equal to the distance from the boundary node to its farthest 'neighbor. This should ensure that the fictitious point does not fall into an element that contains the boundary node. The velocity at the fictitious point is determined by interpolation. "
            
            elif IBTYPEtemp == 41:
                 row2.BndType ="a zero normal velocity gradient boundary. The GWCE is forced with normal flux. The momentum eqs are sacrificed in favor of eqs that set the velocity gradient normal to the boundary equal to zero in the Galerkin sense."
            
            else:
                 row2.BndType ="external boundary with periodic non-zero normal flow combined with wave radiation normal to the boundary as natural boundary conditions and no constraint on the tangential flow. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a periodic river inflow or open ocean boundary with a weak specified normal flow condition and free tangential slip where waves are allowed to propagate freely out of the domain. Discharges are specified in the Model Parameter and Periodic Boundary Condition File as harmonic discharge forcing. Additional parameters, including DRampExtFlux and FluxSettlingTime must also be set in the Model Parameter and Periodic Boundary Condition File in order to use this boundary type."

            cur2.insertRow(row2)

        #print (pnt.Y)
        
    #HERE*****1,4,5,11,21,24,25,

        if IBTYPEtemp in internalList:    
            pnt.X = float(tempX)
            pnt.Y = float(tempY)
            array.add(pnt)
            
        #print (pnt.Y)
        #print ('************************')
        
        row = cur.newRow()
        row.shape = array
        row.segment = long(seg)
        seg = seg+1
        row.IBTYPE = long(IBTYPEtemp)


        
        
        # This condition to include the correct description of IBTYPE from ADCIRC Manual
        
        if IBTYPEtemp == 0:
            row.BndType = "external boundary with no normal flow as an essential boundary condition and no constraint on tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation and by zeroing the normal velocity in the momentum equations. This boundary condition should satisfy no normal flow in a global sense and no normal flow at each boundary node. This type of boundary represents a mainland boundary with a strong no normal flow condition and free tangential slip."

        elif IBTYPEtemp == 1:
             row.BndType = "internal boundary with no normal flow treated as an essential boundary condition and no constraint on the tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation and by zeroing the normal velocity in the momentum equations. This boundary condition should satisfy no normal flow in a global sense and no normal flow at each boundary node. This type of boundary represents an island boundary with a strong normal flow condition and free tangential slip."

        elif IBTYPEtemp == 2: 
            row.BndType ="external boundary with non-zero normal flow as an essential boundary condition and no constraint on the tangential flow. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation and by specifying the non-zero normal velocity in the momentum equations. This boundary condition should correctly satisfy the flux balance in a global sense and the normal flux at each boundary node. This type of boundary represents a river inflow or open ocean boundary with a strong specified normal flow condition and free tangential slip. Discharges are specified either in the Model Parameter and Periodic Boundary Condition File for harmonic discharge forcing or in the Non-periodic, Normal Flux Boundary Condition File for time series discharge forcing."
        
        elif IBTYPEtemp == 3: 
            row.BndType ="external barrier boundary with either zero or non-zero normal outflow from the domain as an essential boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation and by specifying the (zero or non-zero) normal velocity in the momentum equations. Non-zero normal flow is computed using a supercritical, free surface weir formula if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense and the normal flux at each boundary node. This type of boundary represents a mainland boundary comprised of a dike or levee with strong specified normal flow condition and free tangential slip. See External Barrier Boundary Note below for further information on exterior barrier boundaries."
        
        elif IBTYPEtemp == 4: 
            row.BndType ="internal barrier boundary with either zero or non-zero normal flow across the barrier as an essential boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation and by specifying the normal velocity (zero or non-zero) in the momentum equations. Non-zero normal flow is compute using either subcritical or supercritical, free surface weir formula (based on the water level on both sides of the barrier) if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This type of boundary represents a dike or levee that lies inside the computational domain with a strong specified normal flow condition and free tangential slip. See Internal Barrier Boundary Note for further information on exterior barrier boundaries."
        
        elif IBTYPEtemp == 5: 
            row.BndType ="internal barrier boundary with additional cross barrier pipes located under the crown.  Cross barrier flow is treated as an essential normal flow boundary condition which leaves/enters the domain on one side of the barrier and enters/leaves the domain on the corresponding opposite side of the barrier flow rate and direction are based on barrier height, surface water elevation on both sides of the barrier, barrier coefficient and the appropriate barrier flow formula.  In addition cross barrier pipe flow rate and direction are based on pipe crown height, surface water elevation on both sides of the barrier, pipe friction coefficient, pipe diameter and the appropriate pipe flow formula.  Free tangential slip is allowed"
        
        elif IBTYPEtemp == 10: 
            row.BndType ="external boundary with no normal and no tangential flow as essential boundary conditions. This is applied by zeroing the normal boundary flux integral in the continuity equation and by setting the velocity = 0 rather than solving momentum equations along the boundary. This boundary condition should satisfy no normal flow in a global sense and zero velocity at each boundary node. This type of boundary represents a mainland boundary with strong no normal flow and no tangential slip conditions."
        
        elif IBTYPEtemp == 11: 
            row.BndType ="internal boundary with no normal and no tangential flow as essential boundary conditions. This is applied by zeroing the normal boundary flux integral in the continuity equation and by setting the velocity = 0 rather than solving momentum equations along the boundary. This boundary condition should correctly satisfy no normal flow in a global sense and zero velocity at each boundary node. This type of boundary represents an island boundary with strong no normal flow and no tangential slip conditions."
        
        elif IBTYPEtemp == 12: 
            row.BndType ="external boundary with non-zero normal and zero tangential flow as an essential boundary condition. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation and by setting the non-zero normal velocity and zero tangential velocity rather than solving momentum equations along the boundary. This boundary condition should correctly satisfy the flux balance in a global sense and the specified normal/zero tangential velocity at each boundary node. This type of boundary represents a river inflow or open ocean boundary in which strong normal flow is specified with no tangential slip. Discharges are specified either in the Model Parameter and Periodic Boundary Condition File for harmonic forcing or in the Non-periodic, Normal Flux Boundary Condition File for time series forcing."
        
        elif IBTYPEtemp == 13: 
            row.BndType ="external barrier boundary with either zero or non-zero normal outflow from the domain and zero tangential flow as essential boundary conditions. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation and by setting the (zero or non-zero) normal velocity and zero tangential velocity rather than solving momentum equations along the boundary. Non-zero normal flow is computed using a supercritical, free surface weir formula if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense and the normal velocity/zero tangential velocity at each boundary node. This type of boundary represents a mainland boundary comprised of a dike or levee with strong specified normal flow and no tangential slip conditions. See External Barrier Boundary Note below for further information on exterior barrier boundaries."
        
        elif IBTYPEtemp == 20: 
            row.BndType ="external boundary with no normal flow as a natural boundary condition and no constraint on tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) applied in the momentum equations. This boundary condition should satisfy no normal flow in a global sense, but will only satisfy no normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a mainland boundary with a weak no normal flow condition and free tangential slip."
        
        elif IBTYPEtemp == 21:
             row.BndType ="internal boundary with no normal flow as a natural boundary condition and no constraint on the tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. This boundary condition should satisfy no normal flow in a global sense but will only satisfy no normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents an island boundary with a weak no normal flow condition and free tangential slip."
        
        elif IBTYPEtemp == 22:
             row.BndType ="external boundary with non-zero normal flow as a natural boundary condition and no constraint on the tangential flow. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a river inflow or open ocean boundary with a weak specified normal flow condition and free tangential slip. Discharges are specified either in the Model Parameter and Periodic Boundary Condition File for harmonic discharge forcing or in the Non-periodic, Normal Flux Boundary Condition File for time series discharge forcing."
        
        elif IBTYPEtemp == 23:
             row.BndType ="external barrier boundary with either zero or non-zero normal outflow from the domain as a natural boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. Non-zero normal flow is computed using a supercritical, free surface weir formula if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a mainland boundary comprised of a dike or levee with a weak specified normal flow condition and free tangential slip. See External Barrier Boundary Note below for further information on exterior barrier boundaries."
        
        elif IBTYPEtemp == 24:
             row.BndType ="internal barrier boundary with either zero or non-zero normal flow across the barrier as a natural boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. Non-zero normal flow is compute using either subcritical or supercritical, free surface weir formula (based on the water level on both sides of the barrier) if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a dike or levee that lies inside the computational domain with a weak specified normal flow condition and free tangential slip. See Internal Barrier Boundary Note below for further information on exterior barrier boundaries."
        
        elif IBTYPEtemp == 25:
             row.BndType ="internal barrier boundary with additional cross barrier pipes located under the crown.  Cross barrier flow is treated as a natural normal flow boundary condition which leaves/enters the domain on one side of the barrier and enters/leaves the domain on the corresponding opposite side of the barrier.  Flow rate and direction are based on barrier height, surface water elevation on both sides of the barrier, barrier coefficient and the appropriate barrier flow formula.  In addition cross barrier pipe flow rate and direction are based on pipe crown height, surface water elevation on both sides of the barrier, pipe friction coefficient, pipe diameter and the appropriate pipe flow formula.  Free tangential slip is allowed."
        
        elif IBTYPEtemp == 30:
             row.BndType ="wave radiation normal to the boundary as a natural boundary condition. This is applied by specifying the contribution to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. The normal flow is computed using a Sommerfield radiation condition. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents an open boundary where waves are allowed to propagate freely out of the domain."
        
        elif IBTYPEtemp == 32:
             row.BndType ="a combined specified normal flux and outward radiating boundary.  The GWCE is forced with the total normal flux computed by adding the specified normal flux and the flux associated with the outward radiating wave. The latter is determine from a Sommerfeld type condition, flux=celerity*wave elevation. The momentum equations are used to compute the velocity field the same as for a nonboundary node."
        
        elif IBTYPEtemp == 40:
             row.BndType ="a zero normal velocity gradient boundary. The GWCE is forced with normal flux, the momentum eqs are sacrificed in favor of setting the velocity at a boundary node equal to the value at a fictitious point inside the domain. The fictitious point lies on the inward directed normal to the boundary a distance equal to the distance from the boundary node to its farthest 'neighbor. This should ensure that the fictitious point does not fall into an element that contains the boundary node. The velocity at the fictitious point is determined by interpolation. "
        
        elif IBTYPEtemp == 41:
             row.BndType ="a zero normal velocity gradient boundary. The GWCE is forced with normal flux. The momentum eqs are sacrificed in favor of eqs that set the velocity gradient normal to the boundary equal to zero in the Galerkin sense."
        
        else:
             row.BndType ="external boundary with periodic non-zero normal flow combined with wave radiation normal to the boundary as natural boundary conditions and no constraint on the tangential flow. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a periodic river inflow or open ocean boundary with a weak specified normal flow condition and free tangential slip where waves are allowed to propagate freely out of the domain. Discharges are specified in the Model Parameter and Periodic Boundary Condition File as harmonic discharge forcing. Additional parameters, including DRampExtFlux and FluxSettlingTime must also be set in the Model Parameter and Periodic Boundary Condition File in order to use this boundary type."

        cur.insertRow(row)
        array.removeAll()

        #cur2.insertRow(row)

    # --------------- # Reading additional boundaries - Eg SWAN 
    line = input.readline()
    counter = counter + 1
    #print (line)
    #print (counter)
    data=line.split()




    if len(data) > 1:
        numfluseg = int(data[0])
        arcpy.AddMessage("Number of additional boundary segments: "+str(numfluseg))
        line = input.readline() 

        for num in range(numfluseg):    
            line = input.readline()
            data=line.split()
            numseg = int(data[0])
            try: 
                IBTYPEtemp = int(data[1])
            except:
                IBTYPEtemp = -9999
            for num2 in range(numseg):
                line = input.readline()
                data=line.split()
                node = int(data[0])-1    
                pnt.X = float(coord[node,0])
                pnt.Y = float(coord[node,1])
                array.add(pnt)
            row = cur.newRow()
            row.shape = array
            row.segment = long(seg)
            seg = seg+1
            row.IBTYPE = long(IBTYPEtemp)
        
        # This condition to include the correct description of IBTYPE from ADCIRC Manual
            
            if IBTYPEtemp == 0:
                row.BndType = "external boundary with no normal flow as an essential boundary condition and no constraint on tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation and by zeroing the normal velocity in the momentum equations. This boundary condition should satisfy no normal flow in a global sense and no normal flow at each boundary node. This type of boundary represents a mainland boundary with a strong no normal flow condition and free tangential slip."

            elif IBTYPEtemp == 1:
                 row.BndType = "internal boundary with no normal flow treated as an essential boundary condition and no constraint on the tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation and by zeroing the normal velocity in the momentum equations. This boundary condition should satisfy no normal flow in a global sense and no normal flow at each boundary node. This type of boundary represents an island boundary with a strong normal flow condition and free tangential slip."

            elif IBTYPEtemp == 2: 
                row.BndType ="external boundary with non-zero normal flow as an essential boundary condition and no constraint on the tangential flow. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation and by specifying the non-zero normal velocity in the momentum equations. This boundary condition should correctly satisfy the flux balance in a global sense and the normal flux at each boundary node. This type of boundary represents a river inflow or open ocean boundary with a strong specified normal flow condition and free tangential slip. Discharges are specified either in the Model Parameter and Periodic Boundary Condition File for harmonic discharge forcing or in the Non-periodic, Normal Flux Boundary Condition File for time series discharge forcing."
            
            elif IBTYPEtemp == 3: 
                row.BndType ="external barrier boundary with either zero or non-zero normal outflow from the domain as an essential boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation and by specifying the (zero or non-zero) normal velocity in the momentum equations. Non-zero normal flow is computed using a supercritical, free surface weir formula if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense and the normal flux at each boundary node. This type of boundary represents a mainland boundary comprised of a dike or levee with strong specified normal flow condition and free tangential slip. See External Barrier Boundary Note below for further information on exterior barrier boundaries."
            
            elif IBTYPEtemp == 4: 
                row.BndType ="internal barrier boundary with either zero or non-zero normal flow across the barrier as an essential boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation and by specifying the normal velocity (zero or non-zero) in the momentum equations. Non-zero normal flow is compute using either subcritical or supercritical, free surface weir formula (based on the water level on both sides of the barrier) if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This type of boundary represents a dike or levee that lies inside the computational domain with a strong specified normal flow condition and free tangential slip. See Internal Barrier Boundary Note for further information on exterior barrier boundaries."
            
            elif IBTYPEtemp == 5: 
                row.BndType ="internal barrier boundary with additional cross barrier pipes located under the crown.  Cross barrier flow is treated as an essential normal flow boundary condition which leaves/enters the domain on one side of the barrier and enters/leaves the domain on the corresponding opposite side of the barrier flow rate and direction are based on barrier height, surface water elevation on both sides of the barrier, barrier coefficient and the appropriate barrier flow formula.  In addition cross barrier pipe flow rate and direction are based on pipe crown height, surface water elevation on both sides of the barrier, pipe friction coefficient, pipe diameter and the appropriate pipe flow formula.  Free tangential slip is allowed"
            
            elif IBTYPEtemp == 10: 
                row.BndType ="external boundary with no normal and no tangential flow as essential boundary conditions. This is applied by zeroing the normal boundary flux integral in the continuity equation and by setting the velocity = 0 rather than solving momentum equations along the boundary. This boundary condition should satisfy no normal flow in a global sense and zero velocity at each boundary node. This type of boundary represents a mainland boundary with strong no normal flow and no tangential slip conditions."
            
            elif IBTYPEtemp == 11: 
                row.BndType ="internal boundary with no normal and no tangential flow as essential boundary conditions. This is applied by zeroing the normal boundary flux integral in the continuity equation and by setting the velocity = 0 rather than solving momentum equations along the boundary. This boundary condition should correctly satisfy no normal flow in a global sense and zero velocity at each boundary node. This type of boundary represents an island boundary with strong no normal flow and no tangential slip conditions."
            
            elif IBTYPEtemp == 12: 
                row.BndType ="external boundary with non-zero normal and zero tangential flow as an essential boundary condition. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation and by setting the non-zero normal velocity and zero tangential velocity rather than solving momentum equations along the boundary. This boundary condition should correctly satisfy the flux balance in a global sense and the specified normal/zero tangential velocity at each boundary node. This type of boundary represents a river inflow or open ocean boundary in which strong normal flow is specified with no tangential slip. Discharges are specified either in the Model Parameter and Periodic Boundary Condition File for harmonic forcing or in the Non-periodic, Normal Flux Boundary Condition File for time series forcing."
            
            elif IBTYPEtemp == 13: 
                row.BndType ="external barrier boundary with either zero or non-zero normal outflow from the domain and zero tangential flow as essential boundary conditions. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation and by setting the (zero or non-zero) normal velocity and zero tangential velocity rather than solving momentum equations along the boundary. Non-zero normal flow is computed using a supercritical, free surface weir formula if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense and the normal velocity/zero tangential velocity at each boundary node. This type of boundary represents a mainland boundary comprised of a dike or levee with strong specified normal flow and no tangential slip conditions. See External Barrier Boundary Note below for further information on exterior barrier boundaries."
            
            elif IBTYPEtemp == 20: 
                row.BndType ="external boundary with no normal flow as a natural boundary condition and no constraint on tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) applied in the momentum equations. This boundary condition should satisfy no normal flow in a global sense, but will only satisfy no normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a mainland boundary with a weak no normal flow condition and free tangential slip."
            
            elif IBTYPEtemp == 21:
                 row.BndType ="internal boundary with no normal flow as a natural boundary condition and no constraint on the tangential flow. This is applied by zeroing the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. This boundary condition should satisfy no normal flow in a global sense but will only satisfy no normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents an island boundary with a weak no normal flow condition and free tangential slip."
            
            elif IBTYPEtemp == 22:
                 row.BndType ="external boundary with non-zero normal flow as a natural boundary condition and no constraint on the tangential flow. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a river inflow or open ocean boundary with a weak specified normal flow condition and free tangential slip. Discharges are specified either in the Model Parameter and Periodic Boundary Condition File for harmonic discharge forcing or in the Non-periodic, Normal Flux Boundary Condition File for time series discharge forcing."
            
            elif IBTYPEtemp == 23:
                 row.BndType ="external barrier boundary with either zero or non-zero normal outflow from the domain as a natural boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. Non-zero normal flow is computed using a supercritical, free surface weir formula if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a mainland boundary comprised of a dike or levee with a weak specified normal flow condition and free tangential slip. See External Barrier Boundary Note below for further information on exterior barrier boundaries."
            
            elif IBTYPEtemp == 24:
                 row.BndType ="internal barrier boundary with either zero or non-zero normal flow across the barrier as a natural boundary condition and no constraint on the tangential flow. This is applied by specifying the contribution (zero or non-zero) to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. Non-zero normal flow is compute using either subcritical or supercritical, free surface weir formula (based on the water level on both sides of the barrier) if the barrier is overtopped. Zero normal flow is assumed if the barrier is not overtopped. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a dike or levee that lies inside the computational domain with a weak specified normal flow condition and free tangential slip. See Internal Barrier Boundary Note below for further information on exterior barrier boundaries."
            
            elif IBTYPEtemp == 25:
                 row.BndType ="internal barrier boundary with additional cross barrier pipes located under the crown.  Cross barrier flow is treated as a natural normal flow boundary condition which leaves/enters the domain on one side of the barrier and enters/leaves the domain on the corresponding opposite side of the barrier.  Flow rate and direction are based on barrier height, surface water elevation on both sides of the barrier, barrier coefficient and the appropriate barrier flow formula.  In addition cross barrier pipe flow rate and direction are based on pipe crown height, surface water elevation on both sides of the barrier, pipe friction coefficient, pipe diameter and the appropriate pipe flow formula.  Free tangential slip is allowed."
            
            elif IBTYPEtemp == 30:
                 row.BndType ="wave radiation normal to the boundary as a natural boundary condition. This is applied by specifying the contribution to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. The normal flow is computed using a Sommerfield radiation condition. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents an open boundary where waves are allowed to propagate freely out of the domain."
            
            elif IBTYPEtemp == 32:
                 row.BndType ="a combined specified normal flux and outward radiating boundary.  The GWCE is forced with the total normal flux computed by adding the specified normal flux and the flux associated with the outward radiating wave. The latter is determine from a Sommerfeld type condition, flux=celerity*wave elevation. The momentum equations are used to compute the velocity field the same as for a nonboundary node."
            
            elif IBTYPEtemp == 40:
                 row.BndType ="a zero normal velocity gradient boundary. The GWCE is forced with normal flux, the momentum eqs are sacrificed in favor of setting the velocity at a boundary node equal to the value at a fictitious point inside the domain. The fictitious point lies on the inward directed normal to the boundary a distance equal to the distance from the boundary node to its farthest 'neighbor. This should ensure that the fictitious point does not fall into an element that contains the boundary node. The velocity at the fictitious point is determined by interpolation. "
            
            elif IBTYPEtemp == 41:
                 row.BndType ="a zero normal velocity gradient boundary. The GWCE is forced with normal flux. The momentum eqs are sacrificed in favor of eqs that set the velocity gradient normal to the boundary equal to zero in the Galerkin sense."
            
            else:
                 row.BndType ="external boundary with periodic non-zero normal flow combined with wave radiation normal to the boundary as natural boundary conditions and no constraint on the tangential flow. This is applied by specifying the non-zero contribution to the normal boundary flux integral in the continuity equation. There is no constraint on velocity (normal or tangential) in the momentum equations. This boundary condition should correctly satisfy the flux balance in a global sense but will only satisfy the normal flow at each boundary node in the limit of infinite resolution. This type of boundary represents a periodic river inflow or open ocean boundary with a weak specified normal flow condition and free tangential slip where waves are allowed to propagate freely out of the domain. Discharges are specified in the Model Parameter and Periodic Boundary Condition File as harmonic discharge forcing. Additional parameters, including DRampExtFlux and FluxSettlingTime must also be set in the Model Parameter and Periodic Boundary Condition File in order to use this boundary type."

            cur.insertRow(row)
            array.removeAll()

    del lineArray, pnt, cur, row, array, cur2, firstPt

    input.close()

    SR = arcpy.SpatialReference(104145)  #change coordinate system here*** 
     
    
    arcpy.DefineProjection_management(newFC, SR)
    arcpy.DefineProjection_management(newFC2, SR)
       
    # Elapse time and finishing script
    arcpy.AddMessage("End of Script, Process Completed Successfully!")
    stopTime = time.clock()
    elapTime = stopTime - startTime
    arcpy.AddMessage("Total time to run the script: " + str(round(elapTime)) + " seconds")
except:
    arcpy.AddMessage("Error while running script...")
