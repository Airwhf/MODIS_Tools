# Modis_Tools

## 运行环境

Linux

python 3.7 or 3.8

conda install gdal

pip install pymodis

## MODIS数据下载地址

https://e4ftl01.cr.usgs.gov/

## 运行
```commandline
python Modis数据重投影和拼接.py [input_directory] [output_directory] [output_resolution] [band]
```

**input_directory**: 输入文件路径 字符串

**output_directory**: 输出文件路径 字符串

**output_resolution**：输出分辨率 浮点型

**band**：获取波段 字符串

## 部分常用数据参数设置

MCD12Q1（下垫面数据类型）：
```commandline
output_resolution: 0.005

band: "( 1 )"
```




