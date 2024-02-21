from pyper.viper_classes import PolhemusViper
import time
import os
import pandas as pd
import numpy as np
import math
import rospy
import tf2_ros
from geometry_msgs.msg import PoseStamped, TransformStamped
from tf.transformations import quaternion_from_matrix, translation_matrix, euler_matrix, quaternion_matrix, concatenate_matrices
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt

viper = PolhemusViper()
viper.connect()
viper.get_units()
# The current position units are: inch
# The current orientation units are: euler_degrees

loop = True

current_dir = os.getcwd()   
child_dir = 'data'
filename = '2023-07-28_03.pkl'
# filename2 = 'data01.csv'
save_path = os.path.join(current_dir, child_dir, filename)
# save_path2 = os.path.join(current_dir, child_dir, filename2)
rospy.init_node("triangle_skeleton")
boradcaster_flag = True
boradcaster_flag2 = True
# time.sleep(1)
rate = rospy.Rate(30)
if boradcaster_flag:
    
    
    buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(buffer)
    br = tf2_ros.TransformBroadcaster()
    t = TransformStamped()

    buffer2 = tf2_ros.Buffer()
    listener2 = tf2_ros.TransformListener(buffer2)
    br2 = tf2_ros.TransformBroadcaster()
    t2 = TransformStamped()
x = 0
df = pd.DataFrame()
df2 = pd.DataFrame()
# while loop:
# boradcaster_flag = False
delta=np.zeros((2400,6))
# while not rospy.is_shutdown() and loop and x<5*240 :
while not rospy.is_shutdown() and loop:
    try:
        current_frame = viper.get_single_pno(pno_mode="standard")
        # print(current_frame)
        
        data = {'sensor_n':current_frame['sensor_n'],
        'frames':current_frame['frames'],
        'time':current_frame['time'],
        'x':current_frame['x']*25.4,
        'y':current_frame['y']*25.4,
        'z':current_frame['z']*25.4,
        'azimuth':current_frame['azimuth'].apply(math.radians),
        'elevation':current_frame['elevation'].apply(math.radians),
        'roll':current_frame['roll'].apply(math.radians)}

        # row = pd.DataFrame(data)
        # df = pd.concat([df, row], ignore_index=True)
        # time.sleep(.1)  
        # t.header.frame_id = "rgb_camera_link"
        rotation_matrix = euler_matrix(math.radians(float(current_frame['roll'].iloc[0])), math.radians(float(current_frame['elevation'].iloc[0])),math.radians(float(current_frame['azimuth'].iloc[0])))
        q = quaternion_from_matrix(rotation_matrix)
        if boradcaster_flag:
            t.header.frame_id = "viper" # rgb_camera_link
            # t.header.frame_id = "panda_link0" # rgb_camera_link
            # t.child_frame_id = "triangle_link"
            t.child_frame_id = "markerFrame"
            t.header.stamp = rospy.Time.now()
            t.transform.translation.x = float(current_frame['x'].iloc[0])*25.4/1000
            t.transform.translation.y = float(current_frame['y'].iloc[0])*25.4/1000
            t.transform.translation.z = float(current_frame['z'].iloc[0])*25.4/1000
            t.transform.rotation.x = q[0]
            t.transform.rotation.y = q[1]
            t.transform.rotation.z = q[2]
            t.transform.rotation.w = q[3]
            br.sendTransform(t)
        

        # rate.sleep()     
        # print(x, float(current_frame['x'].iloc[0])*25.4, float(current_frame['y'].iloc[0])*25.4, float(current_frame['z'].iloc[0])*25.4, math.radians(float(current_frame['roll'].iloc[0])), math.radians(float(current_frame['elevation'].iloc[0])), math.radians(float(current_frame['azimuth'].iloc[0])))
        # print("{:.2f}".format(float(current_frame['x'].iloc[0])*25.4), "{:.2f}".format(float(current_frame['y'].iloc[0])*25.4), "{:.2f}".format(float(current_frame['z'].iloc[0])*25.4), end=' ')
        # print("{:.2f}".format(float(current_frame['roll'].iloc[0])), "{:.2f}".format(float(current_frame['elevation'].iloc[0])), "{:.2f}".format(float(current_frame['azimuth'].iloc[0])))
        
        translation = [float(current_frame['x'].iloc[0])*25.4, float(current_frame['y'].iloc[0])*25.4, float(current_frame['z'].iloc[0])*25.4]
        # translation = [float(current_frame['x'].iloc[0]), float(current_frame['y'].iloc[0]), float(current_frame['z'].iloc[0])]
        translation_matrix_1 = translation_matrix(translation)
        T1 = concatenate_matrices(translation_matrix_1, rotation_matrix)

        rotation_matrix_2 = euler_matrix(math.radians(float(current_frame['roll'].iloc[1])), math.radians(float(current_frame['elevation'].iloc[1])),math.radians(float(current_frame['azimuth'].iloc[1])))
        q2 = quaternion_from_matrix(rotation_matrix_2)
        translation_2 = [float(current_frame['x'].iloc[1])*25.4, float(current_frame['y'].iloc[1])*25.4, float(current_frame['z'].iloc[1])*25.4]
        # translation_2 = [float(current_frame['x'].iloc[1]), float(current_frame['y'].iloc[1]), float(current_frame['z'].iloc[1])]
        translation_matrix_2 = translation_matrix(translation_2)
        T2 = concatenate_matrices(translation_matrix_2, rotation_matrix_2)



        if boradcaster_flag2:
            t2.header.frame_id = "viper" # rgb_camera_link
            # t.header.frame_id = "panda_link0" # rgb_camera_link
            # t.child_frame_id = "triangle_link"
            t2.child_frame_id = "markerFrame_2"
            t2.header.stamp = rospy.Time.now()
            t2.transform.translation.x = float(current_frame['x'].iloc[1])*25.4/1000
            t2.transform.translation.y = float(current_frame['y'].iloc[1])*25.4/1000
            t2.transform.translation.z = float(current_frame['z'].iloc[1])*25.4/1000
            t2.transform.rotation.x = q2[0]
            t2.transform.rotation.y = q2[1]
            t2.transform.rotation.z = q2[2]
            t2.transform.rotation.w = q2[3]
            br.sendTransform(t2)


        T1_inv = np.linalg.inv(T1)  # 计算逆矩阵
        T_diff = np.dot(T1_inv, T2) # 计算差值矩阵
        R_diff = T_diff[:3, :3]     # 提取旋转矩阵和平移向量
        r = Rotation.from_matrix(R_diff)    # 计算旋转矩阵的欧拉角表示
        rpy_diff = r.as_euler('xyz', degrees=True)
        trans_diff = T_diff[:3, 3]
        res = list(trans_diff) + list(rpy_diff)
        # print(f'** res : {res} **', end=' ')
        # for i in range(len(res)):
        print('ind:', x,'trans_diff:',"{:.2f}".format(res[0]), end=' ')
        print("{:.2f}".format(res[1]), end=' ')
        print("{:.2f}".format(res[2]), end=' mm  | rot_diff: ')
        print("{:.2f}".format(res[3]), end=' ')
        print("{:.2f}".format(res[4]), end=' ')
        print("{:.2f}".format(res[5]), ' degree')
        # print(res)
        # delta.append(res)
        # delta[:,x] = res
        # euler = [float(current_frame['roll'].iloc[0]), float(current_frame['elevation'].iloc[0]),float(current_frame['azimuth'].iloc[0])]
        # euler_2 = [float(current_frame['roll'].iloc[1]), float(current_frame['elevation'].iloc[1]),float(current_frame['azimuth'].iloc[1])]

        # difference = [translation_2[i] - translation[i] for i in range(len(translation))]
        # difference2 = [euler_2[i] - euler[i] for i in range(len(euler))]
        # res = list(difference)+list(difference2)
        # # print(list(difference)+list(difference2))
        # print('trans_diff:',"{:.2f}".format(res[0]), end=' ')
        # print("{:.2f}".format(res[1]), end=' ')
        # print("{:.2f}".format(res[2]), end=' mm  | rot_diff: ')
        # print("{:.2f}".format(res[3]), end=' ')
        # print("{:.2f}".format(res[4]), end=' ')
        # print("{:.2f}".format(res[5]), ' degree')
        # print(res)
        data2 = {'frames':current_frame['frames'].iloc[0],
        'time':current_frame['time'].iloc[0],
        'x':[res[0]],
        'y':[res[1]],
        'z':[res[2]],
        'roll':[res[3]],
        'pitch':[res[4]],
        'yaw':[res[5]],}
        row = pd.DataFrame(data2)
        df2 = pd.concat([df2, row], ignore_index=True)
        
        x+=1
    except BaseException as e:
        # 如果用户按下Ctrl+C，退出程序  
        if isinstance(e, KeyboardInterrupt):
            loop = False
            # df.to_pickle(save_path)
            print(f"Program terminated by user. and save to: {save_path}")
        else:
            pass
    # if boradcaster_flag:
    rate.sleep()

df2.to_pickle(save_path)
print(f"Program terminated by user. and save to: {save_path}")


#------------------------------------------- process data from pickle -----------------------------------------#
data = df2

length = len(df2)

name_dic = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']

print('min:',np.min(delta[:,0]),'max:',np.max(delta[:,0]), 'mean:',np.mean(delta[:,0]), 'std:' ,np.std(delta[:,0]))
print('min:',np.min(delta[:,1]),'max:',np.max(delta[:,1]), 'mean:',np.mean(delta[:,1]), 'std:' ,np.std(delta[:,1]))
print('min:',np.min(delta[:,2]),'max:',np.max(delta[:,2]), 'mean:',np.mean(delta[:,2]), 'std:' ,np.std(delta[:,2]))


#------------------------------------------- plot and print results as table -----------------------------------------#

# set save path
child_dir = 'figures'
filename_table = 'viper_linux_' + filename[:-4] + '_table.png'
save_path_table = os.path.join(current_dir, child_dir, filename_table)

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





# df = pd.DataFrame()
# print(1,result)
# for i in range(len(result)):

#     # df_frame = extract_data_from_acceleration_frame(result[i], "continuous", orientation="euler_degrees", conv_factor=viper.conf['conversion_factor']['euler_degrees'])
#     # df = pd.concat([df, df_frame], ignore_index=True)
#     # df.to_pickle(save_path)
#     # df.to_p
# for i in range(len(result)):

#     # df_frame = extract_data_from_acceleration_frame(result[i], "continuous", orientation="euler_degrees", conv_factor=viper.conf['conversion_factor']['euler_degrees'])
#     # df = pd.concat([df, df_frame], ignore_index=True)
#     # df.to_pickle(save_path)
#     # df.to_pickle(save_path2)
#     print(i, result[i])
# while True:
#     # 读取一条数据
#     data = viper.get_single_pno(pno_mode="standard")

#     # 打印数据
#     print(data)

# import tf
# from tf.transformations import translation_matrix, quaternion_matrix, concatenate_matrices

# # 获取平移矩阵
# translation = [1.0, 2.0, 3.0]
# translation_matrix = translation_matrix(translation)

# # 获取旋转矩阵
# rotation = [0., 0., 0., 1.]
# rotation_matrix = quaternion_matrix(rotation)

# # 获取T矩阵
# T_matrix = concatenate_matrices(translation_matrix, rotation_matrix)

# print(T_matrix)
