### csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
# from scipy.spatial.transform import Rotation
from ast import literal_eval as leval
from os.path import join
import time
import math
import rospy
import tf2_ros
from geometry_msgs.msg import PoseStamped, TransformStamped
from tf.transformations import quaternion_from_matrix, translation_matrix, euler_matrix, quaternion_matrix, concatenate_matrices
from scipy.spatial.transform import Rotation
from matplotlib.font_manager import FontProperties

#------------------------------------------- read data from csv and set save path -----------------------------------------#
current_dir = os.getcwd()
child_dir = 'data'
# filename = 'data09.pkl'
filename = '2023-07-28_02.pkl'
# filename = 'viper_test_T_diff_240hz3.csv'
read_path = os.path.join(current_dir, child_dir, filename)
# filename = 'viper_test_T_diff_240hz3.csv'
df_origin = pd.read_pickle(read_path)

# set save path
child_dir = 'figures'
filename_table = 'viper_linux_' + filename[:-4] + '_table.png'
save_path_table = os.path.join(current_dir, child_dir, filename_table)

filename = 'viper_linux_' + filename[:-4] + '.png'
save_path_figure = os.path.join(current_dir, child_dir, filename)

#------------------------------------------- process data from csv -----------------------------------------#
# df = np.asarray(df_origin)

#------------------------------------------- process data from pickle -----------------------------------------#
data = df_origin

length = len(df_origin)

name_dic = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']

#------------------------------------------- print results version 1 -----------------------------------------#
# for index, name in enumerate(Diff):
#     mean_value = np.mean(data[name])
#     std_deviation = np.std(data[name])
#     print(name,'_diff', end=' : ')
#     print("min : ", "{:.3f}".format(np.min(data[name])), end=' ')
#     print("max : ", "{:.3f}".format(np.max(data[name])), end=' ')
#     print("abs(max-min) : ", "{:.3f}".format(np.abs(np.max(data[name]) - np.min(data[name]))), end=' ')
#     print( "均值：", "{:.3f}".format(mean_value), end='  ')
#     print("标准差：", "{:.3f}".format(std_deviation))

#------------------------------------------- plot and print results as table -----------------------------------------#
from tabulate import tabulate

table_data = []
for index, name in enumerate(name_dic):
    if index < 3:
        unit = ' (mm)'
    else:
        unit = ' (degree)'
    tmp = [name+unit, "{:.3f}".format(np.min(data[name])), "{:.3f}".format(np.max(data[name])), "{:.3f}".format(np.abs(np.max(data[name]) - np.min(data[name]))), "{:.3f}".format(np.mean(data[name])), "{:.3f}".format(np.std(data[name]))]
    table_data.append(tmp)

# only for print version 1
# table = tabulate(table_data, headers=["difference", "min", "max", "|max-min|", "mean", "std"], tablefmt="grid")
# print(table)

headers=["difference", "min", "max", "|max-min|", "mean", "std"]
# 将表格数据转换为2D列表，添加表头
table_data_with_headers = [headers] + table_data

# 使用tabulate函数将表格数据转换为字符串
table_str = tabulate(table_data_with_headers, tablefmt="grid")
print(table_str)

# 绘制表格图
fig_table, ax_table = plt.subplots()
ax_table.axis('off')
table = ax_table.table(cellText=table_data_with_headers, loc='center', cellLoc='center', colLabels=None)

# 调整字体大小和行距
table.auto_set_font_size(False)
table.set_fontsize(30)  # 设置字体大小为14
table.scale(5.0, 5.0)   # 放大表格以增加行距

# 保存为图片
plt.savefig(save_path_table, bbox_inches='tight')
print(save_path_table)

#------------------------------------------- plot data -----------------------------------------#
# length = len(data['x'])
x = np.linspace(0,length/240.0,length)
# x=range(length)
y1 = data['x']
y2 = data['y']
y3 = data['z']
y4 = data['roll']
y5 = data['pitch']
y6 = data['yaw']

fig, axes = plt.subplots(2,3,figsize=(16*1.2,9*1.2))

axes[0, 0].plot(x, y1, label='x_diff')
axes[0, 0].legend()
axes[0, 0].set_title('x_diff')
axes[0, 1].plot(x, y2, label='y_diff')
axes[0, 1].legend()
axes[0, 1].set_title('y_diff')
axes[0, 2].plot(x, y3, label='z_diff')
axes[0, 2].legend()
axes[0, 2].set_title('z_diff')

axes[1, 0].plot(x, y4, label='roll_diff')
axes[1, 0].legend()
axes[1, 0].set_title('roll_diff')
axes[1, 1].plot(x, y5, label='roll_diff')
axes[1, 1].legend()
axes[1, 1].set_title('pitch_diff')
axes[1, 2].plot(x, y6, label='yaw_diff')
axes[1, 2].legend()
axes[1, 2].set_title('yaw_diff')

print(save_path_figure)
plt.savefig(save_path_figure)
# plt.show()