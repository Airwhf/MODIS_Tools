import pymodis
import os
import sys

# 设置modis输入路径
# input_dir = '/mnt/d/2020_MODIS_AOD/ModisLandCover'
input_dir = sys.argv[1]
# 设置GTiff输出路径
# output_dir = '/mnt/d/2020_MODIS_AOD/ModisLandCover/output'
output_dir = sys.argv[2]
# 设置输出分辨率
# res = 0.005
res = sys.argv[3]
# 设置波段
subset = sys.argv[4]
# subset = "( 1 )"

# 建立file_list
# file_list = []
for sname in os.listdir(input_dir):
    if sname[-4::] == '.hdf':
        file_name = f'{input_dir}/{sname}'
        # file_list.append(file_name)
        convert = pymodis.convertmodis_gdal.convertModisGDAL(file_name, f'{output_dir}/{sname[17:23]}', subset, res,
                                                             outformat='GTiff', epsg=4326, wkt=None,
                                                             resampl='NEAREST_NEIGHBOR', vrt=False)
        convert.run()

cmd = f'gdal_merge.py -o mergeLandCover.tif {output_dir}/*'
print(f'若需要对批处理结果进行拼接，在Linux终端使用命令：\n'
      f'{cmd}')






