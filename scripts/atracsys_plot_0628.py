# plot with rotation
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.spatial.transform import Rotation
from ast import literal_eval as leval
from os.path import join


current_dir = os.getcwd()
child_dir = 'python/scripts/data'
filename = 'data15.csv'
save_path = os.path.join(current_dir, child_dir, filename)

# data = pd.read_pickle('~/Atracsys/fusionTrack_SDK-v4.7.4-linux64/python/scripts/data11.pkl')
# data = pd.read_csv('~/Atracsys/fusionTrack_SDK-v4.7.4-linux64/python/scripts/data14.csv')
data = pd.read_csv(save_path)


timestamp = data.iloc[:,0]
marker_id = np.array(data.iloc[:,1])

# data.insert('found_marker_rotation_dim0', '2')
# for ind, row in data.iterrow:

length=len(timestamp)
initial_time = timestamp[0]
x = np.zeros(timestamp.shape)
for i in range(length):
    x[i] = timestamp[i]-initial_time
x_temp = np.zeros((length+1,))
x_temp[1:] = x
x_diff = np.diff(x_temp)

R = np.zeros((length,3,3))
y1 = np.array(data.CoordX)
y2 = np.array(data.CoordY)
y3 = np.array(data.CoordZ)
R[:,0,0] = data.iloc[:,6]
R[:,0,1] = data.iloc[:,7]
R[:,0,2] = data.iloc[:,8]
R[:,1,0] = data.iloc[:,9]
R[:,1,1] = data.iloc[:,10]
R[:,1,2] = data.iloc[:,11]
R[:,2,0] = data.iloc[:,12]
R[:,2,1] = data.iloc[:,13]
R[:,2,2] = data.iloc[:,14]

r =Rotation.from_matrix(R)
rpy = r.as_euler('xyz',degrees=True)

fig2, axes2 = plt.subplots(3,3,figsize=(16,9))
# fig2, axes2 = plt.subplots(3,3)
axes2[0, 0].plot(x, y1, label='x')
axes2[0, 0].legend()
axes2[0, 1].plot(x, y2, label='y')
axes2[0, 1].legend()
axes2[0, 2].plot(x, y3, label='z')
axes2[0, 2].legend()

axes2[1, 0].plot(x, rpy[:,0], label='eular_x')
axes2[1, 0].legend()
axes2[1, 1].plot(x, rpy[:,1], label='eular_y')
axes2[1, 1].legend()
axes2[1, 2].plot(x, rpy[:,2], label='eular_z')
axes2[1, 2].legend()

axes2[2, 1].plot(x[10:], x_diff[10:], label='timestamp_diff')
axes2[2, 1].legend()
axes2[2, 2].plot(x[10:], 1/(x_diff[10:]), label='hz')
axes2[2, 2].legend()
axes2[2, 0].plot(x, marker_id, label='marker_id')
axes2[2, 0].legend()

current_dir = os.getcwd()
child_dir = 'python/scripts/figures'
# print(current_dir)
# filename = 'python/scripts/my_figure.png'
filename = 'atracsys_linux_' + filename[:-4] + '.png'
save_path = os.path.join(current_dir, child_dir, filename)
# save_path = '/python/script/atracsys_linux_0626.png'
# print(save_path)
# save_path ='/home/jn/Atracsys/fusionTrack_SDK-v4.7.4-linux64/python/scripts/atracsys_linux_0628.png'
# plt.savefig(save_path)
# plt.savefig(join(current_dir,filename))
plt.savefig(save_path)


# plt.show()