## Import VTK
from vtk import *

colors = vtkNamedColors()
### Data
#########################
p0 = [0,0,0]
p1 = [0,1,0]
p2 = [1,1,0]
p3 = [0,1,0]

### Create points
################################
points = vtkPoints()
points.InsertNextPoint(p0)
points.InsertNextPoint(p1)
points.InsertNextPoint(p2)
points.InsertNextPoint(p3)

### Create polyline
################################
polyLine = vtkPolyLine()
polyLine.GetPointIds().SetNumberOfIds(5)

## Adding line segments counter clockwise
polyLine.GetPointIds().SetId(0, 0)
polyLine.GetPointIds().SetId(1, 1)
polyLine.GetPointIds().SetId(2, 2)
polyLine.GetPointIds().SetId(3, 3)
polyLine.GetPointIds().SetId(0, 4)


### Create a cell array to store the lines
##########################################
cells = vtkCellArray()
cells.InsertNextCell(polyLine)
# print(polyLine)

### Create polydata
####################
pdata = vtkPolyData()

### Add points and cells to polydata
####################################
pdata.SetPoints(points)
pdata.SetLines(cells)

mapper = vtkPolyDataMapper()
mapper.SetInputData(pdata)

actor = vtkActor()
actor.SetMapper(mapper)

r = vtkRenderer()
rw = vtkRenderWindow()
r.SetBackground(colors.GetColor3d("black"))
rw.AddRenderer(r)
rwi = vtkRenderWindowInteractor()
rwi.SetRenderWindow(rw)
r.AddActor(actor)

rw.Render()
rwi.Start()

### Store the polydata into a vtkpolydata file with extension .vtp
###################################################################
writer = vtkXMLPolyDataWriter()
writer.SetInputData(pdata)
writer.SetFileName('polyline.vtp')
writer.Write()