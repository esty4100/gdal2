from itertools import groupby
from osgeo import gdal
import numpy as np
import sys
# Task a
# convert jpg to tiff


def ConvertToTiff(raster):
    src = gdal.Open(raster)
    newRaster = raster.split(".")[0]+".tiff"
    gdal.Translate(newRaster, src)
    return newRaster


def GetSizeOfRaster(fileUrl):
    raster = gdal.Open(fileUrl)
    xres, yres = raster.GetGeoTransform()[1:6:4]
    width = raster.RasterXSize*xres
    height = raster.RasterYSize*yres
    print(raster.ReadAsArray())
    print(raster.GetGeoTransform())
    print("RasterCountr:", raster.RasterCount)
    return width * height


def GetTheBiggestRaster(raster1, raster2):
    raster1 = ConvertToTiff(raster1)
    raster2 = ConvertToTiff(raster2)
    raster1Size = GetSizeOfRaster(raster1)
    raster2Size = GetSizeOfRaster(raster2)
    return 1 if (raster1Size > raster2Size) else 2

# print(GetTheBiggestRaster("1.jpg","3.jpg"))

# Task b


def CropRaster(raster, point1, point2):
    upper_left_x, upper_left_y = point1
    lower_right_x, lower_right_y = point2
    window = (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
    gdal.Translate("crop"+raster, raster, projWin=window)

# ConvertToTiff("crop2.jpg")
# ConvertToTiff("crop3.jpg")
# print(help(gdal.WarpOptions), options=gdal.WarpOptions(geoloc=True, format='JPEG')
# g = gdal.Warp("output.jpg", ["crop2.jpg","crop3.jpg"])
# CropRaster("2.jpg",(0,0),(2560.0,720.0))
# CropRaster("3.jpg",(0,0),(2560.0,744.0))


g = None

# משימה ב


def IsGray(rgb):
    if all(element == rgb[0] for element in rgb):
        return True
    return False


# path = ConvertToTiff('pic4.jpg')
# print('path:',path)
raster = gdal.Open('pic4.tiff')

band1 = raster.GetRasterBand(1).ReadAsArray()
band2 = raster.GetRasterBand(2).ReadAsArray()
band3 = raster.GetRasterBand(3).ReadAsArray()
rgb_array = np.dstack([band1, band2, band3])
mask = gdal.Open('pic4.tiff.msk',1)
print(type(mask))
print(mask.RasterCount)
# print(mask.ReadAsArray())
counter = 0
array_mask = mask.ReadAsArray()
array_raster = raster.ReadAsArray()
# print(dir(array_mask))


def MarkGrayPixels(array_mask):
    for i in range(len(array_mask)):
        for j in range(len(array_mask[i])):
            if IsGray(rgb_array[i][j]):
                array_mask[i][j] = 1
    print("counter", counter)


def FindTheWay(arrayMask):
    maxArr = []
    arr = []
    tempArr = []
    for i in range(len(arrayMask)):
        for j in range(len(arrayMask[i])):
            if (arrayMask[i][j] == 1):
                arr.append([i, j])
            else:
                if (arr != []):
                    if (len(arr) > len(tempArr)):
                        tempArr = arr
                    arr = []
        if (len(arr) < len(tempArr)):
            arr = tempArr
        if (len(arr) > len(maxArr)):
            maxArr = arr
        arr = []
    return maxArr


def MarkWay(array_mask):
    way = FindTheWay(array_mask)
    row = way[0][0]
    for i in range(len(way)):
        array_mask[row][way[i][1]] = 2
    

MarkGrayPixels(array_mask)
MarkWay(array_mask)
lengthWay = 0
for i in range(len(array_mask)):
    for pixel in array_mask[i]:
        if pixel == 2:
            lengthWay+=1
            print( i, pixel)

print("lengthway:",lengthWay)
mask.GetRasterBand(1).WriteArray(array_mask)
mask.FlushCache()