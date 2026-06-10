# -*- coding: utf-8 -*-
# Python 2.7
from imp import reload
import arcpy
import os
from arcpy.sa import *
import sys  # reload()之前必须要引入模块
from glob import glob

reload(sys)
#sys.setdefaultencoding('utf-8')
arcpy.CheckOutExtension("Spatial")

##读取原始数据文件
def listRaster(AHI_path):
    arcpy.env.workspace = AHI_path
    rasterList = arcpy.ListRasters()
    num = 0
    for raster in rasterList:
        print(raster)
        num += 1
    print('Numbers: ', num)
    print('-' * 50)
    return rasterList

##裁剪栅格数据
def clipRaster(prjList, clip_path, AHI_path, inMaskData):
    if not os.path.exists(clip_path):
        os.makedirs(clip_path)
    arcpy.env.workspace = AHI_path
    num = 0
    for inRaster in prjList:
        # Execute ExtractByMask
        arcpy.env.snapRaster = inRaster
        clip_name = inRaster[:-4] + '.tif'
        # clip_name = u_file[:-4] + '.tif'
        prj_clip = clip_path + '\\' + clip_name
        outClip = ExtractByMask(inRaster, inMaskData)
        outClip.save(prj_clip)
        num += 1
        print(clip_name)
    print('Numbers: ', num)
    print('-' * 50)

def main():
    ##数据目录,需要修改

    AHI_path = r"F:\Academic\BC\clip\old"


    ##裁剪区域，需要修改
    inMaskData = r"F:\Academic\BC\clip\shp\huanan.shp"

    ##临时文件，自动创建
    clip_path = r"F:\Academic\BC\clip\new"

    rasterList = listRaster(AHI_path)
    clipRaster(rasterList, clip_path, AHI_path, inMaskData)


if __name__ == "__main__":
    main()
