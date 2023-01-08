from rasterio.merge import merge
from osgeo import gdal
import numpy as np
import sys
from PIL import Image
# Task a

# convert jpg to tiff
def ConvertToTiff(raster):
    src = gdal.Open(raster)
    if src is None:
        return "No such file or directory"
    newRaster = raster.split(".")[0]+".tiff"
    gdal.Translate(newRaster, src)
    if gdal.Open(newRaster) != None:
        return newRaster
    else:
        print("failed to translate!")
        return "failed to translate!"


def GetSizeOfRaster(fileUrl):
    raster = gdal.Open(fileUrl)
    if raster is None:
        return "No such file or directory"
    xres, yres = raster.GetGeoTransform()[1:6:4]
    width = raster.RasterXSize*xres
    height = raster.RasterYSize*yres
    return width * height


def GetTheBiggestRaster(raster1, raster2):
    raster1Size = GetSizeOfRaster(raster1)
    raster2Size = GetSizeOfRaster(raster2)
    return 1 if (raster1Size > raster2Size) else 2


# Task b

def CropRaster(raster, point1, point2):
    upper_left_x, upper_left_y = point1
    lower_right_x, lower_right_y = point2
    window = (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
    gdal.Translate(raster.split('/')[0]+'/crop'+raster.split('/')[1], raster, projWin = window)


CropRaster("pictures/image1.tif",(696278.000, 3668042.000),( 700374.000,3665994.000))
CropRaster("pictures/image2.tif",(700373.500, 3663946.500),(704469.500,3661898.500))
g = gdal.Warp("pictures/output.jpg", ["pictures/image1.jpg","pictures/image2.jpg"])
g = None

# משימה ב

def IsGray(rgb):
    if all(element == rgb[0] for element in rgb):
        return True
    return False


def MarkGrayPixels(array_mask, rgb_array):
    for i in range(len(array_mask)):
        for j in range(len(array_mask[i])):
            if IsGray(rgb_array[i][j]):
                array_mask[i][j] = 1
    return array_mask


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
    return array_mask


def SetDataToMask(raster, mask):
    dsRaster = gdal.Open(raster)
    band1 = dsRaster.GetRasterBand(1).ReadAsArray()
    band2 = dsRaster.GetRasterBand(2).ReadAsArray()
    band3 = dsRaster.GetRasterBand(3).ReadAsArray()
    rgb_array = np.dstack([band1, band2, band3])
    dsMask = gdal.Open(mask)
    array_mask = dsMask.ReadAsArray()
    MarkGrayPixels(array_mask,rgb_array)
    MarkWay(array_mask)
    return array_mask


def GetWay(raster):
    raster = ConvertToTiff(raster)
    src = gdal.Open(raster,1)
    src.CreateMaskBand(gdal.GMF_NODATA)
    array_mask = SetDataToMask(raster, raster+'.msk')
    mask_raster = gdal.Open(raster+'.msk',1)
    mask_raster.GetRasterBand(1).WriteArray(array_mask)

# GetWay('pictures/pic4.tiff')

