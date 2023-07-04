# plot data without data
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data = pd.read_csv('~/Atracsys/fusionTrack_SDK-v4.7.4-linux64/python/scripts/data10.csv')
timestamp = data.iloc[:,0]
marker_id = np.array(data.iloc[:,2])
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

marker_num = 6
marker = []
for i in range(marker_num):
    marker_tmp = []
    for j in range(length):
        # marker_tmp.append([float(num) for num in marker2_data[i][1:-1].split(',')])
        # marker_tmp.append([float(num) for num in data.iloc[:,i+1][i][1:-1].split(',')])
        tmp = data.iloc[:,i+1+2]
        marker_tmp.append([float(num) for num in tmp[j][1:-1].split(',')])
    marker.append(marker_tmp)
# np.shape(marker)

fig, axes = plt.subplots(3,2,figsize=(10,12))
for i in range(1, marker_num):
    axes[0, 0].plot(x, [inner_list[0] for inner_list in marker[i]], label='marker'+str(i))
    axes[0, 0].legend()
    axes[0, 1].plot(x, [inner_list[1] for inner_list in marker[i]], label='marker'+str(i))
    axes[0, 1].legend()
    axes[1, 0].plot(x, [inner_list[2] for inner_list in marker[i]], label='marker'+str(i))
    axes[1, 0].legend()
axes[1, 1].plot(x[10:], x_diff[10:], label='timestamp_diff')
axes[1, 1].legend()
axes[2, 1].plot(x[10:], 1/(x_diff[10:]), label='hz')
axes[2, 1].legend()
axes[2, 0].plot(x, marker_id, label='marker_id')
axes[2, 0].legend()

# plot 
i=0
fig2, axes2 = plt.subplots(3,2,figsize=(10,12))
axes2[0, 0].plot(x, [inner_list[0] for inner_list in marker[i]], label='marker'+str(i))
axes2[0, 0].legend()
axes2[0, 1].plot(x, [inner_list[1] for inner_list in marker[i]], label='marker'+str(i))
axes2[0, 1].legend()
axes2[1, 0].plot(x, [inner_list[2] for inner_list in marker[i]], label='marker'+str(i))
axes2[1, 0].legend()
axes2[1, 1].plot(x[10:], x_diff[10:], label='timestamp_diff')
axes2[1, 1].legend()
axes2[2, 1].plot(x[10:], 1/(x_diff[10:]), label='hz')
axes2[2, 1].legend()
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