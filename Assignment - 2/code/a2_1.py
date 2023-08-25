# Importing vtk
from vtk import *

# Importing colors 
colors = vtkNamedColors()

# Initializing XMLImageDataReader object
reader = vtkXMLImageDataReader()

# Setting filename and updating
reader.SetFileName('./Isabel_2D.vti')
reader.Update()

# Taking out ouput from the reader
data = reader.GetOutput()

# Finding out the number of cells using GetNumberOfCells() function and printing it
cells = data.GetNumberOfCells()
print('Number of cells :', cells)

# Taking out the pressure values (scalar) from the data named 'Pressure'
pressureArray = data.GetPointData().GetArray('Pressure')

# Taking isovalue as an input
C = int(input('Enter the iso value : '))


# Defining a helper function
# It takes the 3D coordinates and pressure value at two points and find the coordinate
# of the point having pressure value = C
def findIsoContourPoint(x1, y1, z1, p1, x2, y2, z2, p2):
    x = (((p1 - C)/(p1-p2)) * (x2-x1)) + x1
    y = (((p1 - C)/(p1-p2)) * (y2-y1)) + y1
    z = (((p1 - C)/(p1-p2)) * (z2-z1)) + z1
    return (x, y, z)

# Defining a global vtkCellArray
cellArray = vtkCellArray()

# Defining a global vtkPolyline
polyLine = vtkPolyLine()

# Defining a global vtkPoints
pts = vtkPoints()

# Defining a global list to contain all the contour points
p = []

# global variable to count the total number of iso points
ptsCount = 0

for id in range(cells):

    # Taking out a cell with id = id
    cell = data.GetCell(id)

    # Getting list of point Ids using GetPointIds() function
    indList = cell.GetPointIds()
    
    # Defining local points list
    points = []
    
    # Using GetId(index) function to get the id stored in indList
    pid1 = indList.GetId(0)
    pid2 = indList.GetId(1)
    pid3 = indList.GetId(3)
    pid4 = indList.GetId(2)

    # Using point ids to get the point 3D coordinate    
    x1,y1,z1 = data.GetPoint(pid1)[0], data.GetPoint(pid1)[1], data.GetPoint(pid1)[2]
    x2,y2,z2 = data.GetPoint(pid2)[0], data.GetPoint(pid2)[1], data.GetPoint(pid2)[2]
    x3,y3,z3 = data.GetPoint(pid3)[0], data.GetPoint(pid3)[1], data.GetPoint(pid3)[2]
    x4,y4,z4 = data.GetPoint(pid4)[0], data.GetPoint(pid4)[1], data.GetPoint(pid4)[2]
    
    # Finding pressure values at each corner point of the cell using point id
    pat1 = pressureArray.GetValue(pid1)
    pat2 = pressureArray.GetValue(pid2)
    pat3 = pressureArray.GetValue(pid3)
    pat4 = pressureArray.GetValue(pid4)

    # Count variable to count the number of iso points in the current cell 
    count = 0

    # 4 Conditions to check one of the following two cases in each edge of the cell in counter-clockwise direction : 
    # 1. left point has greater value than C and right point has smaller value than C
    # 2. right point has greater value than C and left point has smaller value than C

    # Edge 1-2
    if((pat1 > C and pat2 < C) or (pat1 < C and pat2 > C)):
        x, y, z = findIsoContourPoint(x1, y1, z1, pat1, x2, y2, z2, pat2)
        points.append([x, y, z])
        p.append([x, y, z])
        count += 1
        
    # Edge 2-3
    if((pat2 > C and pat3 < C) or (pat2 < C and pat3 > C)):
        x, y, z = findIsoContourPoint(x2, y2, z2, pat2, x3, y3, z3, pat3)
        points.append([x, y, z])
        p.append([x, y, z])
        count += 1
    
    # Edge 3-4
    if((pat3 > C and pat4 < C) or (pat3 < C and pat4 > C)):
        x, y, z = findIsoContourPoint(x3, y3, z3, pat3, x4, y4, z4, pat4)
        points.append([x, y, z])
        p.append([x, y, z])
        count += 1
    
    # Edge 4-1
    if((pat4 > C and pat1 < C) or (pat4 < C and pat1 > C)):
        x, y, z = findIsoContourPoint(x4, y4, z4, pat4, x1, y1, z1, pat1)
        points.append([x, y, z])
        p.append([x, y, z])
        count += 1
    
    for j in range(0, count, 2):
        polyLine.GetPointIds().SetNumberOfIds(2)
        polyLine.GetPointIds().SetId(0, ptsCount)
        polyLine.GetPointIds().SetId(1, ptsCount+1)
        ptsCount += 2
        cellArray.InsertNextCell(polyLine)
        
# Inserting all the points in the vtkPoints        
for i in range(ptsCount):
    pts.InsertNextPoint(p[i])
print(ptsCount)


# Defining a vtkPolyData
pdata = vtkPolyData()

# Setting up points in the polydata
pdata.SetPoints(pts)

# Setting up lines in the polydata
pdata.SetLines(cellArray)

# As per the vtk pipeline defining polyDataMapper which maps data to graphic domain
# and setting the input as the filter output
mapper = vtkPolyDataMapper()

# Setting input in the mapper
mapper.SetInputData(pdata)

# Defining the actor, which are the objects with certain geometry and properties
actor = vtkActor()

# Setting up the mapper in the actor
actor.SetMapper(mapper)

# Defining renderer which renders the actor
r = vtkRenderer()

# Defining render window where renderer will render the actor
rw = vtkRenderWindow()

# Adding background to the renderer object
r.SetBackground(colors.GetColor3d("black"))

# Adding renderer in the render window
rw.AddRenderer(r)

# Defining the Render Window Interactor through which we can interact with the objects by rotating or scaling them
rwi = vtkRenderWindowInteractor()

# Setting the render window in the render window interactor
rwi.SetRenderWindow(rw)

# Adding actor in the renderer
r.AddActor(actor)

# Setting up full screen to render 
rw.SetFullScreen(True)

# Setting up the border so that it's convinient to close the graphic screen
# Without it we will not see the minimize or close button 
rw.SetBorders(True)

# Defining vtkXMLPolyDataWriter
writer = vtkXMLPolyDataWriter()

# Setting input data in the writer
writer.SetInputData(pdata)

# Setting the filename
writer.SetFileName('contour.vtp')

# Writing the polydata
writer.Write()

# Starting render process in the render window
rw.Render()

# Starting the interaction part
rwi.Start()