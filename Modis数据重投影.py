import pymodis
import os
import glob

# 设置modis输入路径
input_dir = r'/mnt/d/Chorme_Download/MCD15A2H_2017_SCB'
# 设置GTiff输出路径
output_dir = r'/mnt/d/Chorme_Download/MCD15A2H_2017_SCB_output'
# 设置输出分辨率
res = 0.005
# 设置波段
subset = "( 0 1 )"

# 创建输出目录
try:
    os.mkdir(output_dir)
except:
    a = None

# 查找时间标识
file_list = glob.glob(f'{input_dir}/*.hdf')
for file_name in file_list:
    sname = os.path.basename(file_name)
    # file_list.append(file_name)
    convert = pymodis.convertmodis_gdal.convertModisGDAL(file_name, f'{output_dir}/{sname}', subset, res,
                                                         outformat='GTiff', epsg=4326, wkt=None,
                                                         resampl='NEAREST_NEIGHBOR', vrt=False)
    convert.run()

cmd = f'gdal_merge.py -o mergeLandCover.tif {output_dir}/*'
print(f'若需要对批处理结果进行拼接，在Linux终端使用命令：\n'
      f'{cmd}')






