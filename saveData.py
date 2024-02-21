from pyper.viper_classes import PolhemusViper
import time
import os
import pandas as pd
import math
import numpy as np
# import rospy
# import tf2_ros
# from geometry_msgs.msg import PoseStamped, TransformStamped
# from tf.transformations import quaternion_from_matrix, translation_matrix

# from pyper.io.decoding_utils import extract_data_from_acceleration_frame
# from threading import Event
# from multiprocessing.pool import ThreadPool

viper = PolhemusViper()
viper.connect()
viper.get_units()

loop = True

current_dir = os.getcwd()
child_dir = 'data'
filename = 'data03.pkl'
# filename2 = 'data01.csv'
save_path = os.path.join(current_dir, child_dir, filename)
# save_path2 = os.path.join(current_dir, child_dir, filename2)

# time.sleep(1)
# rospy.init_node("triangle_skeleton")
# rate = rospy.Rate(60)
# buffer = tf2_ros.Buffer()
# listener = tf2_ros.TransformListener(buffer)
# br = tf2_ros.TransformBroadcaster()
# t = TransformStamped()
x = 0
df = pd.DataFrame()
while loop:
# while not rospy.is_shutdown() and loop:
    try:
        current_frame = viper.get_single_pno(pno_mode="standard",)
        print(current_frame)
        
        # data = {'sensor_n':current_frame['sensor_n'],
        # 'frames':current_frame['frames'],
        # 'time':current_frame['time'],
        # 'x':float(current_frame['x'].iloc[0])*25.4,
        # 'y':float(current_frame['y'].iloc[0])*25.4,
        # 'z':float(current_frame['z'].iloc[0])*25.4,
        # 'azimuth':math.radians(float(current_frame['azimuth'].iloc[0])),
        # 'elevation':math.radians(float(current_frame['elevation'].iloc[0])),
        # 'roll':math.radians(float(current_frame['roll'].iloc[0]))}
        # print(data)
        data = {'sensor_n':current_frame['sensor_n'],
        'frames':current_frame['frames'],
        'time':current_frame['time'],
        'x':current_frame['x']*25.4,
        'y':current_frame['y']*25.4,
        'z':current_frame['z']*25.4,
        'azimuth':current_frame['azimuth'].apply(math.radians),
        'elevation':current_frame['elevation'].apply(math.radians),
        'roll':current_frame['roll'].apply(math.radians)}
        # print(data)
        row = pd.DataFrame(data)
        # row = pd.DataFrame(current_frame)
        df = pd.concat([df, row], ignore_index=True)
        # time.sleep(.1)       
    except BaseException as e:
        # 如果用户按下Ctrl+C，退出程序  
        if isinstance(e, KeyboardInterrupt):
            loop = False
            df.to_pickle(save_path)
            print(f"Program terminated by user. and save to: {save_path}")
        else:
            pass


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