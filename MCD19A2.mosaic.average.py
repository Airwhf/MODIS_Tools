import os.path
import glob
import numpy as np
import rasterio
from osgeo import gdal
import datetime


def yyyyddd_to_yyyymmdd(yyyyddd):
    yyyy = yyyyddd[0:4]
    ddd = int(yyyyddd[4:7])
    start_date = f'{yyyy}-01-01'
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    yyyymmdd = start_date + datetime.timedelta(days=ddd-1)
    yyyymmdd = datetime.datetime.strftime(yyyymmdd, '%Y%m%d')
    return yyyymmdd


def write_band(file_name, output_name):
    # file_name = r'D:\MODIS\geo_out\MCD19A2.A2015060.h27v07.006.2018102053601.hdf.tif'
    with rasterio.open(file_name) as dataset:
        out_meta = dataset.meta
        band1 = dataset.read(1)  # 后续更新需改为均值
        transform = dataset.transform
        out_meta.update({"driver": "GTiff",
                         "height": band1.shape[0],
                         "width": band1.shape[1],
                         "count": 1,
                         "dtype": band1.dtype,
                         "transform": transform})
    with rasterio.open(output_name, "w", **out_meta) as dataset:
        dataset.write(band1, 1)


def calculated_average(file_list, output_name):
    # 获取元数据
    with rasterio.open(file_list[0]) as dataset:
        out_meta = dataset.meta
        band1 = dataset.read()
        transform = dataset.transform
        out_meta.update({"driver": "GTiff",
                         "height": band1.shape[0],
                         "width": band1.shape[1],
                         "count": 1,
                         "dtype": band1.dtype,
                         "transform": transform})

    sum = np.zeros(band1.shape)  # 总量
    num = np.zeros(band1.shape)  # 计数
    for file_name in file_list:
        with rasterio.open(file_name) as dataset:
            out_meta = dataset.meta
            band1 = dataset.read(1)
        sum = sum + band1
        temp_num = np.where(band1 == 0, 0, 1)
        num = num + temp_num
    num = np.where(num == 0, 1, num)
    average = sum/num
    with rasterio.open(output_name, "w", **out_meta) as dataset:
        dataset.write(average[0, :, :], 1)
    return average


def main(date_label, input_directory, output_directory):
    # 设置拼接后的数据输出范围
    lon_min = 67.0
    lon_max = 140.0
    lat_min = 15.0
    lat_max = 60.0

    yyyymmdd = yyyyddd_to_yyyymmdd(date_label)
    #  gdal打开hdf数据集
    os.chdir(input_directory)
    file_list = glob.glob(f"*{date_label}*.hdf")
    for i in file_list:
        TifName = f"{output_directory}/{os.path.basename(i)}.tif"
        # 跳过已经处理过的结果
        if os.path.exists(TifName):
            print(f'The image {TifName} is already exists in the directory.')
            continue
        datasets = gdal.Open(i)
        #  获取hdf中的子数据集
        SubDatasets = datasets.GetSubDatasets()
        Metadata = datasets.GetMetadata()
        #  打印元数据
        # for key, value in Metadata.items():
        #     print('{key}:{value}'.format(key=key, value=value))
        #  获取要转换的子数据集
        data = datasets.GetSubDatasets()[1][0]
        # print(datasets.GetSubDatasets()[1][0])
        Raster_DATA = gdal.Open(data)
        DATA_Array = Raster_DATA.ReadAsArray()[0, :, :]
        # print(Raster_DATA)
        # print(DATA_Array.shape)
        #  保存为tif
        geoData = gdal.Warp(TifName, Raster_DATA,
                            dstSRS='EPSG:4326', format='GTiff',
                            resampleAlg=gdal.GRA_Bilinear)
        del geoData
        write_band(TifName, TifName)
        print(f'Finish the single image process and output {TifName}')

    # 拼接
    # 跳过已经拼接过的结果
    if os.path.exists(f'{output_directory}/mosaic/mosaic_{yyyymmdd}.tif'):
        print(f'The mosaic in {yyyymmdd} have already processed.')
        return
    # 创建拼接结果存放路径
    if os.path.exists(f'{output_directory}/mosaic') is False:
        os.mkdir(f'{output_directory}/mosaic')
    cmd = f'gdal_merge.py -o {output_directory}/mosaic/mosaic_{yyyymmdd}.tif ' \
          f'-n -28672 -ps 0.01 0.01 ' \
          f'-ul_lr {lon_min} {lat_max} {lon_max} {lat_min}'

    file_list = glob.glob(f'{output_directory}/MCD19A2.A{date_label}*.tif')
    for file_name in file_list:
        cmd = f'{cmd} {file_name}'
    os.system(cmd)
    print(f'---------------------------------------------------')
    print(f'Finish the image mosaic in {yyyymmdd}.')
    print(f'---------------------------------------------------')


if __name__ == "__main__":
    # ********************** scale factor = 0.001 **********************
    input_directory = '/mnt/d/MODIS'
    output_directory = '/mnt/d/MODIS/geo_band'

    if os.path.exists(output_directory) is False:
        os.mkdir(output_directory)
    # 获取所有时间标识
    modis_data = glob.glob(f'{input_directory}/*.hdf')
    date_label_list = []
    for temp_modis_data in modis_data:
        temp_date_label = os.path.basename(temp_modis_data)[9:16]
        if date_label_list.__contains__(temp_date_label) is False:
            date_label_list.append(temp_date_label)
    for date_label in date_label_list:
        main(date_label, input_directory, output_directory)

    # 计算月均值
    avr_dir = f'{output_directory}/average'
    if os.path.exists(avr_dir) is False:
        os.mkdir(avr_dir)
    year = '2015'
    month_arr = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for month in month_arr:
        file_list = glob.glob(f'{output_directory}/mosaic/mosaic_{year}{month}*.tif')
        if len(file_list) != 0:
            output_name = f'{avr_dir}/average_{year}{month}.tif'
            average = calculated_average(file_list, output_name)
            print(f'Finish the average calculated and output {output_name}')






