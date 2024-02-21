#! /user/bin/python

"""
Example showing how to initialise, configure, and communicate
with NDI Polaris, Vega, and Aurora trackers.
"""
import time
import six
from sksurgerynditracker.nditracker import NDITracker
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os
from collections import deque
from scipy.spatial.transform import Rotation
import time
import pandas as pd
import numpy as np

from tkinter import Y
# import cv2
import rospy
import tf2_ros
import numpy as np
# import pykinect_azure as pykinect
# from pykinect_azure import K4A_CALIBRATION_TYPE_COLOR, K4A_CALIBRATION_TYPE_DEPTH, k4a_float2_t
from geometry_msgs.msg import PoseStamped, TransformStamped
from tf.transformations import quaternion_from_matrix, translation_matrix

if __name__ == "__main__":
# current_dir = os.getcwd()
# child_dir = 'scripts/data'
# filename = 'data11.pkl'
# save_path = os.path.join(current_dir, child_dir, filename)

    settings_vega = {
        "tracker type": "vega",
        "ip address": "169.254.7.99",
        "port" : 8765,
        "romfiles" : [
            "./data/0703.rom"]
        }

    tracker = NDITracker(settings_vega)
    tracker.start_tracking()

    six.print_(tracker.get_tool_descriptions())

# df = pd.DataFrame()
# x = 0

# for i in range(600):
# # while True:    
#     current_frame = tracker.get_frame()
#     print(x)
#     x += 1
#     data = {'timestamp':current_frame[1],
#     'found_marker_id':current_frame[0],
#     'Tmat':current_frame[3],
#     'error':current_frame[4],
#     'frame_num':current_frame[2]}
            
#     row = pd.DataFrame(data)
#     df = pd.concat([df, row], ignore_index=True)

# df.to_pickle(save_path)
# tracker.stop_tracking()
# tracker.close()


    rospy.init_node("triangle_skeleton")
    rate = rospy.Rate(60)
    buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(buffer)
    br = tf2_ros.TransformBroadcaster()
    t = TransformStamped()
    x = 0

    while not rospy.is_shutdown():
        current_frame = tracker.get_frame()
        data = {'timestamp':current_frame[1],
        'found_marker_id':current_frame[0],
        'Tmat':current_frame[3],
        'error':current_frame[4],
        'frame_num':current_frame[2]}

        # t.header.frame_id = "rgb_camera_link"
        t.header.frame_id = "NDI_vega" # rgb_camera_link
        # t.child_frame_id = "triangle_link"
        t.child_frame_id = "markerFrame"
        t.header.stamp = rospy.Time.now()
        t.transform.translation.x = np.array(current_frame[3])[:,0,3]/1000
        t.transform.translation.y = np.array(current_frame[3])[:,1,3]/1000
        t.transform.translation.z = np.array(current_frame[3])[:,2,3]/1000
        transformation_matrix = np.eye(4)
        transformation_matrix[0, :4] = np.array(current_frame[3])[:,0,:4]
        transformation_matrix[1, :4] = np.array(current_frame[3])[:,1,:4]
        transformation_matrix[2, :4] = np.array(current_frame[3])[:,2,:4]
        transformation_matrix[3, :4] = np.array(current_frame[3])[:,3,:4]
        q = quaternion_from_matrix(transformation_matrix)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        br.sendTransform(t)
        rate.sleep()
        print(x, np.array(current_frame[3])[:,0,3], np.array(current_frame[3])[:,1,3], np.array(current_frame[3])[:,2,3])
        # print(np.array(current_frame[3])[:,:3,:3])
        # print(transformation_matrix)
        x+=1