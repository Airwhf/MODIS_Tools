import glob
import os

# 输入数据目录
input_dir = r'/mnt/d/Chorme_Download/MCD15A2H_2017_SCB_output'
output_dir = r'/mnt/d/Chorme_Download/MCD15A2H_2017_SCB_output_merge'

# 创建输出目录
try:
    os.mkdir(output_dir)
except:
    a = None
#
file_list = glob.glob(f'{input_dir}/*.tif')
# 截取时间标识符
times_labels = []
for file_name in file_list:
    sname = os.path.basename(file_name)[9:17]
    times_labels.append(sname)
    # print(sname)
# 拼接数据
for times_label in times_labels:
    file_list = glob.glob(f'{input_dir}/*.{times_label}.*.tif')
    cmd = f'gdal_merge.py -o {output_dir}/{times_label}.tif'
    for file_name in file_list:
        cmd = f'{cmd} {file_name}'
    # print(cmd)
    os.system(cmd)



