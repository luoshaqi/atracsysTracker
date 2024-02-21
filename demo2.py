from pyper.viper_classes import PolhemusViper
import time
import os

viper = PolhemusViper()
viper.connect()
viper.get_units()

current_dir = os.getcwd()
child_dir = 'data'
filename = 'data01.pkl'
filename2 = 'data01.csv'
save_path = os.path.join(current_dir, child_dir, filename)
save_path2 = os.path.join(current_dir, child_dir, filename2)
import pandas as pd

from pyper.io.decoding_utils import extract_data_from_acceleration_frame

from threading import Event
from multiprocessing.pool import ThreadPool

viper.start_continuous(pno_mode="standard", frame_counting="reset_frames") # "reset_frames" means that the first frame after starting the continuous mode will have an index == 0

stop_event = Event()
pool = ThreadPool(processes=1)
async_result = pool.apply_async(viper.read_continuous, [stop_event])

time.sleep(2)

stop_event.set()
result = async_result.get()

df = pd.DataFrame()
print(len(result))
for i in range(len(result)):

    df_frame = extract_data_from_acceleration_frame(result[i], "continuous", orientation="euler_degrees", conv_factor=viper.conf['conversion_factor']['euler_degrees'])
    df = pd.concat([df, df_frame], ignore_index=True)
    df.to_pickle(save_path)
    df.to_pickle(save_path2)
    # print(i, result[i])