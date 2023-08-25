# Importing vtk
from vtk import *
import random
from scipy.interpolate import griddata
import numpy as np
import time

samplingPercentage = int(input('Enter sampling percentage : ').strip())
interpolationMethod = input('Enter method (linear/nearest):').strip()

# Getting out polydata from 3d isabel image data

# Importing colors 
colors = vtkNamedColors()

# Initializing XMLImageDataReader object
reader = vtkXMLImageDataReader()

# Setting filename and updating
reader.SetFileName('./Isabel_3D.vti')
reader.Update()

# Taking out ouput from the reader
data = reader.GetOutput()

# Getting pressure array values
pressureArray = data.GetPointData().GetArray('Pressure')

# Getting total number of points
numOfPoints = data.GetNumberOfPoints()

# Finding the dimension of the data set
(xDim, yDim, zDim) = data.GetDimensions()


# Function to find the indices of the corner point and return it in a set
def enterDefaultValues():

    # Initializing a set
    a = set({})
    
    t = data.FindPoint(0, 0, 0)
    a.add(t)
    
    t = data.FindPoint(xDim-1, 0, 0)
    a.add(t)

    t = data.FindPoint(xDim-1, yDim-1, 0)
    a.add(t)

    t = data.FindPoint(0, yDim-1, 0)
    a.add(t)
    
    t = data.FindPoint(0, 0, zDim-1)
    a.add(t)

    t = data.FindPoint(xDim-1, 0, zDim-1)
    a.add(t)

    t = data.FindPoint(xDim-1, yDim-1, zDim-1)
    a.add(t)

    t = data.FindPoint(0, yDim-1, zDim-1)
    a.add(t)
    
    return a


# percentage to return the sampled indices in the form of a set
def srs(percentage):

    # getting total number of sampled points
    numberOfSampledPoints = int((numOfPoints * percentage)/100)

    # storing corner indices in indices variable
    indices = enterDefaultValues()
    
    # As long as we don't get the required amount of sample points keep finding the random numbers
    while(len(indices) < numberOfSampledPoints):
        rp = random.randint(0, numOfPoints)
        indices.add(rp)

    # return indices
    return indices


# function to compute snr
def compute_snr(arrgt, arr_recon):
    diff = arrgt - arr_recon
    sqd_max_diff = (np.max(arrgt)-np.min(arrgt))**2
    snr = 10 * np.log10(sqd_max_diff/np.mean(diff**2))
    return snr

# storing sampled points index in sampledSet
sampledSet = srs(samplingPercentage)

# converting set into list
sampledPoints = list(sampledSet)

# getting total number of sampled points
numOfSampledPoints = len(sampledPoints)

# defining list
sampledValues = []
sampledCoord = []

# getting sampled points value and their coordinates
for val in sampledPoints:
    sampledValues.append(pressureArray.GetValue(val))
    sampledCoord.append(data.GetPoint(val))

# defining vtkfloatArray as well as vtkPoints
arr = vtkFloatArray()
points = vtkPoints()

# storing the values and coordinates in vtk format
for i in range(numOfSampledPoints):
    arr.InsertNextValue(sampledValues[i])
    points.InsertNextPoint(sampledCoord[i])

# setting the array name
arr.SetName('Pressure')
    
# defining poly data and setting its attributes
pdata = vtkPolyData()
pdata.SetPoints(points)
pdata.GetPointData().SetScalars(arr)

# defining vtkXMLPolyDataWriter and writing sample.vtp
writer = vtkXMLPolyDataWriter()
writer.SetInputData(pdata)
writer.SetFileName('sample.vtp')
writer.Write()

# defining array to store value and coordinates of all the points
allPoints = []
allValues = []

# getting value and coordinates of all the points
for i in range(numOfPoints):
    allPoints.append(data.GetPoint(i))
    allValues.append(pressureArray.GetValue(i))

# using scipy.interpolate.griddata to get interpolated values
if interpolationMethod == 'nearest':
    startTime = time.time()
    reconstructedDataValueList = griddata(sampledCoord, sampledValues, (allPoints), method="nearest")
    endTime = time.time()
else:
    startTime = time.time()
    reconstructedDataValueList = griddata(sampledCoord, sampledValues, (allPoints), method="linear")
    updatedList = []
    updatedCoord = []
    for i in range(numOfPoints):
        if(not (np.isnan(reconstructedDataValueList[i]) == True)):
            updatedList.append(reconstructedDataValueList[i])
            updatedCoord.append(data.GetPoint(i))
    reconstructedDataValueList = griddata(updatedCoord, updatedList, (allPoints), method="nearest")
    endTime = time.time()


reconstructedDataValueVtkArray = vtkFloatArray()
for i in range(numOfPoints):
    reconstructedDataValueVtkArray.InsertNextValue(reconstructedDataValueList[i])
reconstructedImage = vtkImageData()
reconstructedImage.SetDimensions(250, 250, 50)
reconstructedImage.GetPointData().SetScalars(reconstructedDataValueVtkArray)

writer = vtkXMLImageDataWriter()
writer.SetFileName("img.vti")
writer.SetInputData(reconstructedImage)
writer.Write()
print("Total time required for interpolation :",endTime - startTime)
print("Signal to Noise Ratio :",compute_snr(np.array(allValues),np.array(reconstructedDataValueList)))