from pyper.viper_classes import PolhemusViper
import time

viper = PolhemusViper()
viper.connect()

viper.get_units()

# The current position units are: cm
# The current orientation units are: euler_degrees

viper.get_single_pno(pno_mode="standard")

# or for PNO frames that also contain acceleration info:
viper.get_single_pno(pno_mode="acceleration")

from threading import Event
from multiprocessing.pool import ThreadPool

viper.start_continuous(pno_mode="acceleration", frame_counting="reset_frames") # "reset_frames" means that the first frame after starting the continuous mode will have an index == 0

stop_event = Event()
pool = ThreadPool(processes=1)
async_result = pool.apply_async(viper.read_continuous, [stop_event])

time.sleep(2)

stop_event.set()
result = async_result.get()

viper.stop_continuous()

import pandas as pd

from pyper.io.decoding_utils import extract_data_from_acceleration_frame


df = pd.DataFrame()
for i in range(len(result)):

    df_frame = extract_data_from_acceleration_frame(result[i], "continuous", orientation="euler_degrees", conv_factor=viper.conf['conversion_factor']['euler_degrees'])
    df = pd.concat([df, df_frame], ignore_index=True)
