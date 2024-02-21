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


def calculate_delta(vector1, vector2):
    rotation_matrix1 = euler_matrix(vector1[3],vector1[4],vector1[5])
    # q1 = quaternion_from_matrix(rotation_matrix1)
    translation1 = [vector1[0],vector1[1],vector1[2]]
    translation_matrix1 = translation_matrix(translation1)
    T1 = concatenate_matrices(translation_matrix1, rotation_matrix1)

    rotation_matrix2 = euler_matrix(vector2[3],vector2[4],vector2[5])
    # q2 = quaternion_from_matrix(rotation_matrix2)
    translation2 = [vector2[0],vector2[1],vector2[2]]
    translation_matrix2 = translation_matrix(translation2)
    T2 = concatenate_matrices(translation_matrix2, rotation_matrix2)
    T1_inv = np.linalg.inv(T1)  # 计算逆矩阵
    T_diff = np.dot(T1_inv, T2) # 计算差值矩阵
    R_diff = T_diff[:3, :3]     # 提取旋转矩阵和平移向量
    r = Rotation.from_matrix(R_diff)    # 计算旋转矩阵的欧拉角表示
    rpy_diff = r.as_euler('xyz', degrees=True)
    trans_diff = T_diff[:3, 3]
    res = list(trans_diff) + list(rpy_diff)
    return res
#------------------------------------------- read data from csv and set save path -----------------------------------------#
current_dir = os.getcwd()
child_dir = 'data'
filename_origin = 'viper_test_T_diff_960hz2.csv'
# filename = 'viper_test_T_diff_240hz2.csv'
# filename_origin = 'viper_test_ftt_on_09.csv'
read_path = os.path.join(current_dir, child_dir, filename_origin)
df_origin = pd.read_csv(read_path)

# set save path
child_dir = 'figures'
filename_table = 'viper_win' + filename_origin[:-4] + '_table.png'
save_path_table = os.path.join(current_dir, child_dir, filename_table)

filename_figure = 'viper_win' + filename_origin[:-4] + '.png'
save_path_figure = os.path.join(current_dir, child_dir, filename_figure)

filename_dist = 'viper_win' + filename_origin[:-4] + '_dist.png'
save_path_figure_dist = os.path.join(current_dir, child_dir, filename_dist)

#------------------------------------------- process data from csv -----------------------------------------#

df = np.asarray(df_origin)

length = len(df)
sensor1 = np.zeros((length,6))
sensor2 = np.zeros((length,6))
distortion = np.zeros((length,2))
for j in range(6):
    if j<3:
        tmp2 = 25.4
    else:
        tmp2 = 1.0
    for i in range(length):
        sensor1[i,0+j]=df[i][7+j]*tmp2
        sensor2[i,0+j]=df[i][19+j]*tmp2
        distortion[i,0] = df[i][5]
        distortion[i,1] = df[i][17]

sensor1[:,[3,4,5]] = sensor1[:,[5,4,3]]
sensor2[:,[3,4,5]] = sensor2[:,[5,4,3]]

diff=np.zeros((length,6))
dist=np.zeros((length,1))
for i in range(length):
    tmp3 = calculate_delta(sensor1[i,:],sensor2[i,:])
    # diff.append(tmp3)
    diff[i,:] = tmp3
    dist[i,:] = np.linalg.norm(sensor1[i,[0,1,2]]-sensor2[i,[0,1,2]])
# diff=sensor1-sensor2


Diff = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']

data={'x':diff[:,0],
    'y':diff[:,1],
    'z':diff[:,2],
    'yaw':diff[:,3],
    'pitch':diff[:,4],
    'roll':diff[:,5],
    }

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
for index, name in enumerate(Diff):
    if index < 3:
        unit = ' (mm)'
    else:
        unit = ' (degree)'
    tmp = [name+unit, "{:.3f}".format(np.min(data[name])), "{:.3f}".format(np.max(data[name])), "{:.3f}".format(np.abs(np.max(data[name]) - np.min(data[name]))), "{:.3f}".format(np.mean(data[name])), "{:.3f}".format(np.std(data[name]))]
    table_data.append(tmp)
    # max_index = np.argmax(np.array(np.abs(np.max(data[name]) - np.min(data[name]))))
    # max_index = np.argmax(data[name])
    # print(name+"最大|max-min|的索引：", max_index, sensor1[max_index,:], sensor2[max_index,:], df_origin.iloc[max_index])
    # print()
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
x = np.linspace(0,length/960.0,length)
# x=range(length)
y1 = diff[:,0]
y2 = diff[:,1]
y3 = diff[:,2]
y4 = diff[:,5]
y5 = diff[:,4]
y6 = diff[:,3]

fig, axes = plt.subplots(2,3,figsize=(16*1.2,9*1.2))

axes[0, 0].plot(x, y1, label='x_diff')
axes[0, 0].plot(x, sensor1[:,0], label='sensor1')
axes[0, 0].plot(x, sensor2[:,0], label='sensor2')
axes[0, 0].legend()
axes[0, 0].set_title('x_diff')

axes[0, 1].plot(x, y2, label='y_diff')
axes[0, 1].plot(x, sensor1[:,1], label='sensor1')
axes[0, 1].plot(x, sensor2[:,1], label='sensor2')
axes[0, 1].legend()
axes[0, 1].set_title('y_diff')

axes[0, 2].plot(x, y3, label='z_diff')
axes[0, 2].plot(x, sensor1[:,2], label='sensor1')
axes[0, 2].plot(x, sensor2[:,2], label='sensor2')
axes[0, 2].legend()
axes[0, 2].set_title('z_diff')


axes[1, 0].plot(x, y4, label='roll_diff')
axes[1, 0].plot(x, sensor1[:,5], label='sensor1')
axes[1, 0].plot(x, sensor2[:,5], label='sensor2')
axes[1, 0].legend()
axes[1, 0].set_title('roll_diff')

axes[1, 1].plot(x, y5, label='roll_diff')
axes[1, 1].plot(x, sensor1[:,4], label='sensor1')
axes[1, 1].plot(x, sensor2[:,4], label='sensor2')
axes[1, 1].legend()
axes[1, 1].set_title('pitch_diff')

axes[1, 2].plot(x, y6, label='yaw_diff')
axes[1, 2].plot(x, sensor1[:,3], label='sensor1')
axes[1, 2].plot(x, sensor2[:,3], label='sensor2')
axes[1, 2].legend()
axes[1, 2].set_title('yaw_diff')


print(save_path_figure)
plt.savefig(save_path_figure)
# plt.show()

fig3, axes3 = plt.subplots(2,1,figsize=(16*1.2,9*1.2))
axes3[0].plot(x, dist[:,0], label='distance')
axes3[0].legend()
axes3[0].set_title('distance')

axes3[1].plot(x, distortion[:,0]/255, label='distortion1')
axes3[1].plot(x, distortion[:,1]/255, label='distortion2')
axes3[1].legend()
axes3[1].set_title('Electromagnetic distortion index (0-1)')

plt.savefig(save_path_figure_dist)
print(save_path_figure_dist)

print(np.max(dist))
print(np.min(dist))
print(np.max(dist)-np.min(dist))