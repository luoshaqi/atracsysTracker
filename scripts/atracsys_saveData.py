import atracsys.stk as tracking_sdk

import platform
if platform.system() == 'Darwin':
    import matplotlib
    matplotlib.use("TkAgg")

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os
from collections import deque
from scipy.spatial.transform import Rotation
import time
import pandas as pd

# Replace atracsys.stk with atracsys.ftk for the fusionTrack.
def exit_with_error(error, tracking_system):
    print(error)
    answer = tracking_system.get_last_error()
    if answer[0] == tracking_sdk.Status.Ok:
        errors_dict = answer[1]
        for level in ['errors', 'warnings', 'messages']:
            if level in errors_dict:
                print(errors_dict[level])
    exit(1)


tracker = tracking_sdk.TrackingSystem()

if tracker.initialise() != tracking_sdk.Status.Ok:
    exit_with_error(
        "Error, can't initialise the atracsys SDK api.", tracker)

if tracker.enumerate_devices() != tracking_sdk.Status.Ok:
    exit_with_error("Error, can't enumerate devices.", tracker)

frame = tracking_sdk.FrameData()
aa = tracking_sdk.Status.Ok
print(tracking_sdk.Status.Ok)
if tracking_sdk.Status.Ok == True:
    print("tracking_sdk.Status.Ok")
else:
    print("tracking_sdk.Status.is not ok")
bb = tracker.create_frame(False, 10, 20, 20, 10)
if tracker.create_frame(False, 10, 20, 20, 10) != tracking_sdk.Status.Ok:
    exit_with_error("Error, can't create frame object. 1", tracker)

answer = tracker.get_enumerated_devices()
if answer[0] != tracking_sdk.Status.Ok:
    exit_with_error("Error, can't get list of enumerated devices", tracker)

print("Tracker with serial ID {0} detected".format(
    hex(tracker.get_enumerated_devices()[1][0].serial_number)))

answer = tracker.get_data_option("Data Directory")
if answer[0] != tracking_sdk.Status.Ok:
    exit_with_error("Error, can't read 'Data Directory' option", tracker)

geometry_path = answer[1]

# for geometry in ['geometry001.ini', 'geometry002.ini', 'geometry003.ini', 'geometry004.ini', 'geometry005.ini']:
for geometry in ['geometry666.ini','geometry667.ini','geometry668.ini','geometry669.ini','geometry670.ini']:
    if tracker.set_geometry(os.path.join(geometry_path, geometry)) != tracking_sdk.Status.Ok:
        exit_with_error("Error, can't create frame object. 2", tracker)

# ------------------------------ initialize 
df = pd.DataFrame()
x = 0
markers_indexes = {}
current_marker_index = 0 # 1
max_number_of_tracked_markers = 5
initial_time = time.time()
# --------------------------------------------------------------------------------------------

for i in range(1000):
# while True:    
    # print(x)
    x += 1
    tracker.get_last_frame(frame)
    marker_data = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0,0,0)]
    found_marker_id = -1
    found_marker_index = -1
    found_marker_data = (0,0,0)
    for marker in frame.markers:
        
        if not marker.geometry_id in markers_indexes:
            markers_indexes[marker.geometry_id] = current_marker_index
            current_marker_index += 1

        if markers_indexes[marker.geometry_id] < max_number_of_tracked_markers:
            r = Rotation.from_matrix(marker.rotation)
            # print(marker.rotation)
            # rpy = r.as_euler('xyz', degrees=True)
            rpy = r.as_euler('zyx', degrees=True)
            marker_data[markers_indexes[marker.geometry_id]] = (
                marker.position[0], marker.position[1], marker.position[2])
                # marker.position[0], marker.position[1], marker.position[2],rpy[0],rpy[1],rpy[2])
                # rpy[0],rpy[1],rpy[2])
            all_zero = all(num == 0 for num in marker_data[markers_indexes[marker.geometry_id]])
            if all_zero == False:
                found_marker_id = marker.geometry_id
                found_marker_index = markers_indexes[found_marker_id]
                found_marker_data = marker_data[found_marker_index]
        
        # print(rpy[0])
        # print(marker.rotation)
        # print(time, )
    print(x, found_marker_id, found_marker_index)
    current_frame_data = (
        x, marker_data[0], marker_data[1], marker_data[2], marker_data[3],marker_data[4])

    data = {'timestamp':time.time(),
            # 'time':(time.time()-initial_time),
            'found_marker_id':[found_marker_id],
            'found_marker_index':[found_marker_index],
            'found_marker_data':[found_marker_data],
            'marker1_data':[marker_data[0]],
            'marker2_data':[marker_data[1]],
            'marker3_data':[marker_data[2]],
            'marker4_data':[marker_data[3]],
            'marker5_data':[marker_data[4]]}
            
    # row = pd.DataFrame(data, index=[0])
    row = pd.DataFrame(data)
    df = pd.concat([df, row], ignore_index=True)
    # time.sleep(.1)

df.to_csv('/home/jn/Atracsys/fusionTrack_SDK-v4.7.4-linux64/python/scripts/data10.csv',index=False)


