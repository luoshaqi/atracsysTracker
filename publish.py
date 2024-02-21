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

viper = PolhemusViper()
viper.connect()
viper.get_units()
# The current position units are: inch
# The current orientation units are: euler_degrees

loop = True

current_dir = os.getcwd()
child_dir = 'data'
filename = 'data05.pkl'
# filename2 = 'data01.csv'
save_path = os.path.join(current_dir, child_dir, filename)
# save_path2 = os.path.join(current_dir, child_dir, filename2)

# time.sleep(1)
rospy.init_node("triangle_skeleton")
rate = rospy.Rate(60)
buffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(buffer)
br = tf2_ros.TransformBroadcaster()
t = TransformStamped()
x = 0
df = pd.DataFrame()
# while loop:
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
        t.header.frame_id = "viper" # rgb_camera_link
        # t.header.frame_id = "panda_link0" # rgb_camera_link
        # t.child_frame_id = "triangle_link"
        t.child_frame_id = "markerFrame"
        t.header.stamp = rospy.Time.now()
        t.transform.translation.x = float(current_frame['x'].iloc[0])*25.4/1000
        t.transform.translation.y = float(current_frame['y'].iloc[0])*25.4/1000
        t.transform.translation.z = float(current_frame['z'].iloc[0])*25.4/1000
        rotation_matrix = euler_matrix(math.radians(float(current_frame['roll'].iloc[0])), math.radians(float(current_frame['elevation'].iloc[0])),math.radians(float(current_frame['azimuth'].iloc[0])))
        q = quaternion_from_matrix(rotation_matrix)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        br.sendTransform(t)
        # rate.sleep()     
        # print(x, float(current_frame['x'].iloc[0])*25.4, float(current_frame['y'].iloc[0])*25.4, float(current_frame['z'].iloc[0])*25.4, math.radians(float(current_frame['roll'].iloc[0])), math.radians(float(current_frame['elevation'].iloc[0])), math.radians(float(current_frame['azimuth'].iloc[0])))
        print("{:.2f}".format(float(current_frame['x'].iloc[0])*25.4), "{:.2f}".format(float(current_frame['y'].iloc[0])*25.4), "{:.2f}".format(float(current_frame['z'].iloc[0])*25.4), end=' ')
        print("{:.2f}".format(float(current_frame['roll'].iloc[0])), "{:.2f}".format(float(current_frame['elevation'].iloc[0])), "{:.2f}".format(float(current_frame['azimuth'].iloc[0])))
        
        

        x+=1
    except BaseException as e:
        # 如果用户按下Ctrl+C，退出程序  
        if isinstance(e, KeyboardInterrupt):
            loop = False
            # df.to_pickle(save_path)
            print(f"Program terminated by user. and save to: {save_path}")
        else:
            pass
    rate.sleep()


# df = pd.DataFrame()
# print(1,result)
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
