# Importing vtk
from vtk import *

# Importing colors 
colors = vtkNamedColors()

# Initializing XMLImageDataReader object
reader = vtkXMLImageDataReader()

# Setting filename and updating
reader.SetFileName('./Isabel_3D.vti')
reader.Update()

# Taking out ouput from the reader
data = reader.GetOutput()

# Defining vtkColorTransferFunction()
colorTransfer = vtkColorTransferFunction()

# Defining vtkPiecewiseFunction()
opacityFun = vtkPiecewiseFunction()

# Setting color space to RGB
colorTransfer.SetColorSpaceToRGB()

# Given rgb colors in a list
rgbColors = [[-4931.54, 0, 1, 1], [-2508.95, 0, 0, 1], [-1873.9, 0, 0, 0.5], [-1027.16, 1, 0, 0], [-298.031, 1, 0.4, 0], [2594.97, 1, 1, 0]]

# Given opacity values in a list
opacityVal = [[-4931.54, 1.0], [101.815, 0.002], [2594.97, 0.0]]

# Adding rgb colors in the color transfer function
for i in range(len(rgbColors)):
    colorTransfer.AddRGBPoint(rgbColors[i][0], rgbColors[i][1], rgbColors[i][2], rgbColors[i][3])

# Adding opacity values in the piecewise function
for i in range(len(opacityVal)):
    opacityFun.AddPoint(opacityVal[i][0], opacityVal[i][1])

# Creating an outline filter
outFilter = vtkOutlineFilter()

# Setting up input data in it and updating it
outFilter.SetInputData(data)
outFilter.Update()

# Defining a vtkPolyDataMapper
mapper = vtkPolyDataMapper()

# Setting input connection in the mapper by getting the output from the filter
mapper.SetInputConnection(outFilter.GetOutputPort())

# Defining a vtkActor
actor = vtkActor()

# Setting mapper in the actor
actor.SetMapper(mapper)

# Setting filter actor to black color i.e. (0, 0, 0) as rgb values
actor.GetProperty().SetColor(0, 0, 0)

# Defining vtkSmartVolumeMapper()
sVolMapper = vtkSmartVolumeMapper()

# Setting up input in the mapper
sVolMapper.SetInputData(data)

# Defining a vtkVolumeProperty object which contains the value of some properties of the volume
volProperty = vtkVolumeProperty()

# Asking input from the user
phongShading = input('Phong shading input(y/n) : ')

# Trimming whitespaces from both the ends of the user input
var = phongShading.strip()

# If user input is 'y' or 'Y' then switch on shading and set up ambient, diffuse and specular values
# else switch shading off
if(var == 'y' or var == 'Y'):
    volProperty.ShadeOn()
    volProperty.SetAmbient(0.5)
    volProperty.SetDiffuse(0.5)
    volProperty.SetSpecular(0.5)
else:
    volProperty.ShadeOff()

# Setting up the opacity property in vtkVolumeProperty
volProperty.SetScalarOpacity(opacityFun)

# Seting up the color property in vtkVolumeProperty
volProperty.SetColor(colorTransfer)

# Defining a vtkVolume (acts as an actor)
vol = vtkVolume()

# Setting vtkSmartVolumeMapper in the volume
vol.SetMapper(sVolMapper)

# Setting up property in the volume defined in volProperty (vtkVolumeProperty)
vol.SetProperty(volProperty)

# Defining renderer which renders the actor
r = vtkRenderer()

# Setting renderer background to be white
r.SetBackground(1,1,1)

# Adding volume as an actor in the renderer
r.AddActor(vol)

# Adding filter actor in the renderer
r.AddActor(actor)

# Defining render window where renderer will render the actor
rw = vtkRenderWindow()

# Adding renderer in the render window
rw.AddRenderer(r)

# Setting up the render window name
if(var == 'y' or var == 'Y'):
    rw.SetWindowName('With phong shading')
else:
    rw.SetWindowName('Without phong shading')

# Defining the Render Window Interactor through which we can interact with the objects by rotating or scaling them
rwi = vtkRenderWindowInteractor()

# Setting the render window in the render window interactor
rwi.SetRenderWindow(rw)

# Setting up the render window size to 1000*1000
rw.SetSize(1000, 1000)

# Starting render process in the render window
rw.Render()

# Starting the interaction part
rwi.Start()