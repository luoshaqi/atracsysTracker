import os
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import json
# from scipy.spatial.transform import Rotation
from ast import literal_eval as leval
from os.path import join

current_dir = os.getcwd()
child_dir = 'data'
filename = 'data05.pkl'
save_path = os.path.join(current_dir, child_dir, filename)
data = pd.read_pickle(save_path)
print(data)

# timestamp = data['timestamp']
# marker_id = data['found_marker_id']
# Tmat_tmp = np.array(data['Tmat'])
# error = data['error']
# frame_num = data['frame_num']

# length=len(timestamp)
# initial_time = timestamp[0]
# x = np.zeros(timestamp.shape)
# for i in range(length):
#     x[i] = timestamp[i]-initial_time
# x_temp = np.zeros((length+1,))
# x_temp[1:] = x
# x_diff = np.diff(x_temp)

# Tmat = np.zeros((length,4,4))
# for i in range(length):
#     Tmat[i,:,:] = Tmat_tmp[i]
# y1 = Tmat[:,0,3]
# y2 = Tmat[:,0,3]
# y3 = Tmat[:,0,3]
  
# rpy = Rotation.from_matrix(Tmat[:,:3,:3]).as_euler('xyz',degrees=True)

# fig, axes = plt.subplots(3,3,figsize=(16*1.2,9*1.2))
# axes[0, 0].plot(x, y1, label='x')
# axes[0, 0].legend()
# axes[0, 0].set_title('position x')
# axes[0, 1].plot(x, y2, label='y')
# axes[0, 1].legend()
# axes[0, 1].set_title('position y')
# axes[0, 2].plot(x, y3, label='z')
# axes[0, 2].legend()
# axes[0, 2].set_title('position y')

# axes[1, 0].plot(x, rpy[:,0], label='eular_x')
# axes[1, 0].legend()
# axes[1, 0].set_title('pose eular_x')
# axes[1, 1].plot(x, rpy[:,1], label='eular_y')
# axes[1, 1].legend()
# axes[1, 1].set_title('pose eular_y')
# axes[1, 2].plot(x, rpy[:,2], label='eular_z')
# axes[1, 2].legend()
# axes[1, 2].set_title('pose eular_z')

# axes[2, 0].plot(x, marker_id, label='marker_id')
# axes[2, 0].legend()
# axes[2, 0].set_title('marker id')
# # axes[2, 1].plot(x[10:], x_diff[10:], label='sampling interval')
# axes[2, 1].plot(x, error, label='error')
# axes[2, 1].legend()
# axes[2, 1].set_title('error')
# axes[2, 2].plot(x[10:], 1/(x_diff[10:]), label='Hz')
# axes[2, 2].legend()
# axes[2, 2].set_title('sampling frequency')

# child_dir = 'scripts/figures'
# filename = 'NDI_linux_' + filename[:-4] + '.png'
# save_path = os.path.join(current_dir, child_dir, filename)

# plt.savefig(save_path)
# plt.show()