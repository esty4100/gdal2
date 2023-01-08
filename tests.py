from app import *

def test_convert():
    assert ConvertToTiff("pictures/pic1.jpg") == "pictures/pic1.tiff"
    assert ConvertToTiff("pictures/x") == "No such file or directory"


def test_size_raster():
    assert GetSizeOfRaster("pictures/pic1.jpg") == 3840000.0
    assert GetSizeOfRaster("pictures/x.jpg") == "No such file or directory"


def test_bigger_raster():
    assert GetTheBiggestRaster("pictures/pic1.jpg","pictures/pic2.jpg") == 1


def test_is_gray():
    assert IsGray([1,1,1]) == True
    assert IsGray([1,2,2]) == False


def test_find_the_way():
    array_mask = [[0,0,1,0],[1,1,1,1],[0,0,0,0],[1,1,0,1]]
    assert FindTheWay(array_mask) == [[1,0],[1,1],[1,2],[1,3]]


def test_mark_way():
    array_mask = [[0,0,1,0],[1,1,1,1],[0,0,0,0],[1,1,0,1]]
    assert MarkWay(array_mask) == [[0,0,1,0],[2,2,2,2],[0,0,0,0],[1,1,0,1]]


def test_mark_gray_pixels():
    array_mask = [[0,0],[0,0]]
    rgb_array = [[[23,23,23],[1,2,3]],[[3,3,3],[3,3,5]]]
    assert MarkGrayPixels(array_mask,rgb_array) == [[1,0],[1,0]]