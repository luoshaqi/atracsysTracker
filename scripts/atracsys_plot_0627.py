# plot with rotation
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.spatial.transform import Rotation
from ast import literal_eval as leval

# data = pd.read_pickle('~/Atracsys/fusionTrack_SDK-v4.7.4-linux64/python/scripts/data11.pkl')
data = pd.read_csv('~/Atracsys/fusionTrack_SDK-v4.7.4-linux64/python/scripts/data11.csv')

# timestamp = leval(data.iloc[:,0])
timestamp = data.iloc[:,0]
marker_id = np.array(data.iloc[:,2])

# data.insert('found_marker_rotation_dim0', '2')
# for ind, row in data.iterrow:


# temp = leval(data.found_marker_rotation.to_list()[0])
# marker1_data = data.iloc[:,1]
# marker2_data = data.iloc[:,2]
length=len(timestamp)
# x = np.linspace(0,10,len(timestamp))
initial_time = timestamp[0]
x = np.zeros(timestamp.shape)
for i in range(length):
    x[i] = timestamp[i]-initial_time
x_temp = np.zeros((length+1,))
x_temp[1:] = x
x_diff = np.diff(x_temp)
# print(time.shape)

marker_num = 0
marker = []
# for i in range(marker_num):
i = 0
marker_tmp = []
marker_rotation_tmp = []
rpy=[]
for j in range(length):
    # marker_tmp.append([float(num) for num in marker2_data[i][1:-1].split(',')])
    # marker_tmp.append([float(num) for num in data.iloc[:,i+1][i][1:-1].split(',')])
    tmp = data.iloc[:,i+1+2]
    marker_tmp.append([float(num) for num in tmp[j][1:-1].split(',')])
    rotation_tmp = data.iloc[:,i+1+2+1]
    # json.loads(rotation_tmp[j])
    # [number for sublist in json.loads(rotation_tmp[j]) for number in sublist]
    tmp2 = [number for sublist in json.loads(rotation_tmp[j]) for number in sublist]
    marker_rotation_tmp.append(np.reshape(tmp2,(3,3)))
    r = Rotation.from_matrix(np.reshape(tmp2,(3,3)))
    rpy.append(r.as_euler('xyz', degrees=True))

    # rpy = r.as_euler('zyx', degrees=True)
marker.append(marker_tmp)

fig2, axes2 = plt.subplots(3,3,figsize=(10,12))
axes2[0, 0].plot(x, [inner_list[0] for inner_list in marker[i]], label='x')
axes2[0, 0].legend()
axes2[0, 1].plot(x, [inner_list[1] for inner_list in marker[i]], label='y')
axes2[0, 1].legend()
axes2[0, 2].plot(x, [inner_list[2] for inner_list in marker[i]], label='z')
axes2[0, 2].legend()

axes2[1, 0].plot(x, np.asarray(rpy)[:,0], label='euler_x')
axes2[1, 0].legend()
axes2[1, 1].plot(x, np.asarray(rpy)[:,1], label='euler_y')
axes2[1, 1].legend()
axes2[1, 2].plot(x, np.asarray(rpy)[:,2], label='euler_z')
axes2[1, 2].legend()

axes2[2, 1].plot(x[10:], x_diff[10:], label='timestamp_diff')
axes2[2, 1].legend()
axes2[2, 2].plot(x[10:], 1/(x_diff[10:]), label='hz')
axes2[2, 2].legend()
axes2[2, 0].plot(x, marker_id, label='marker_id')
axes2[2, 0].legend()


# plt.show()
# current_dir = os.getcwd()
# print(current_dir)
# filename = 'my_figure.png'
# save_path = os.path.join(current_dir, '/python/scripts', filename)
# save_path = '/python/script/atracsys_linux_0626.png'
# print(save_path)
save_path ='/home/jn/Atracsys/fusionTrack_SDK-v4.7.4-linux64/python/scripts/atracsys_linux_0626.png'
# plt.savefig(save_path)

plt.show()