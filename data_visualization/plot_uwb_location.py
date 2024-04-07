

import datetime as dt
import os

import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

import time
from datetime import datetime

from scipy.signal import butter, filtfilt
from scipy.signal import lfilter, freqz

# Function to design a low-pass Butterworth filter
def butter_lowpass(cutoff, fs, order=2):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

# Function to apply a filter to a signal
def butter_lowpass_filter(data, cutoff, fs, order=2):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Design a high-pass Butterworth filter
def butter_highpass(cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

# Apply the high-pass filter to the signal
def butter_highpass_filter(data, cutoff, fs, order=4):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def search_files(folder_path, search_text):
    file_names = []
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"): # Check if the file is a text file
            if search_text in file_name: # Check if the search text is present in the file name
                file_names.append(file_name)
    return sorted(file_names)

def datetime_to_unix_timestamp(datetime_str):
    datetime_obj = datetime.strptime(datetime_str, ' %Y/%m/%d %H:%M:%S') # Parse the datetime string into a datetime object
    unix_timestamp = int(time.mktime(datetime_obj.timetuple())) # Convert the datetime object to a Unix timestamp
    return unix_timestamp

def read_text_timestamp(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            row_values = line.strip().split(',')
            first_column = int(row_values[0])
            second_column = row_values[1]
            third_column = row_values[2]
            data.append((first_column, second_column, third_column))
    numpy_array = np.array(data)
    return numpy_array


# ===============================================
""" Main program from here """

current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory
project_dir = os.path.dirname(current_dir)   # Get the parent directory (one level up)
project_dir = os.path.dirname(project_dir)   # Get the parent directory (one level up)
project_dir = os.path.dirname(project_dir) 


tag_id = 2
date = "0725"

# timestamp_file = project_dir + "/timestamps_processing.txt"
# timestamp_file = project_dir + "/timestamps_start_stop.txt"

# time_data = read_text_timestamp(timestamp_file)

tag_name = f'T{tag_id:02d}' 
print('\nTag: ' + tag_name)
cow_name = f'C{tag_id:02d}'

# """ Ploting location data """  
# location_in_3D = np.empty((0,5))

# selected_name_extension = "_z_opt"
# selected_name_extension = "_NLoS"
# selected_name_extension = "location_data_T02_0725_50"
# selected_name_extension = "_z_opt"

# name_extension_list = ["_z_opt"]
# name_extension_list = ["_NLoS"]
# name_extension_list = ["_z_opt", "_NLoS"]
list_file_name = ["triangulation/location_data_T02_0725_tri0.csv",
                  "gd_data/location_data_T02_0725_2_groups_T1.csv"]
# list_file_name = ["gd_data/location_data_T02_0725_2_groups_T1.csv",
#                   "gd_data/location_data_T02_0725_2_groups_T2.csv",
#                   "gd_data/location_data_T02_0725_2_groups_T3.csv",
#                   "gd_data/location_data_T02_0725_2_groups_T4.csv",
#                   "gd_data/location_data_T02_0725_all_groups_T5.csv"]

# list_file_name = ["triangulation/location_data_T02_0725_tri0.csv",
#                   "triangulation/location_data_T02_0725_tri10.csv",
#                   "triangulation/location_data_T02_0725_tri20.csv",
#                   "triangulation/location_data_T02_0725_tri30.csv",
#                   "triangulation/location_data_T02_0725_tri50.csv"]

# for selected_name_extension in name_extension_list:
for input_file_name in list_file_name:
    # input_file_name = "/location_data_" + tag_name + '_' + date + selected_name_extension + ".csv"                  
    dataset = "/location_data/"

    print('File: ' + input_file_name)
    file_path = project_dir + dataset + tag_name + '/' + input_file_name

    df = pd.read_csv(file_path) # skip the firt row, otherwise: header = True
    data = 0
    data = df.to_numpy()

    timestamps = data[:,0]
    locations = data[:,13:16]

    plt.figure(figsize=(6, 6))
    
    plot_data = True

    """ Ploting ankle data """
    plot_ankle = True
    if plot_ankle and plot_data:
        # Get standing reference
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory
            project_dir = os.path.dirname(current_dir)   # Get the parent directory (one level up)
            input_file_dir = project_dir + "/CPS_cow_data_v1/standing_reference/" + cow_name + "_" + date + ".csv"
            ref_data = pd.read_csv(input_file_dir).values[:,0:2].astype(int)
        except:
            print("No standing reference")
            ref_data = np.ones((len(timestamps), 2)).astype(int)

        standing_timestamps = ref_data[:,0]
        standing = ref_data[:,1]

        datet = [dt.datetime.fromtimestamp(ts) for ts in standing_timestamps]
        plt.plot(datet, standing, color='orange', label='standing')
    
    # Adding timestamp to the location
    data = np.hstack((timestamps[:, np.newaxis], locations))

    ## Filter outliner
    loc_list = []
    for loc in data:
        x_m = loc[1]
        y_m = loc[2]
        z_m = loc[3]
        if np.abs(x_m) < 11 and np.abs(y_m) < 8 and z_m > 0 and z_m < 2:
            loc_list.append(loc)
    locations = np.asarray(loc_list).reshape((-1, 4))

    locations = data # Without filtering outliners

    timestamps = locations[:,0]
    x_m = locations[:,1]
    y_m = locations[:,2]
    z_m = locations[:,3]

    timestamp = [dt.datetime.fromtimestamp(ts) for ts in timestamps]

    # Plot soothed z axis
    if plot_data:
        # LPF
        # cutoff_frequency = 0.1 # Cutoff frequency in Hz
        # sampling_rate = 10
        # signal = butter_lowpass_filter(z_m, cutoff_frequency, sampling_rate) 

        # Apply a moving average filter for smoothing
        window_size = 50
        signal = np.convolve(z_m, np.ones(window_size)/window_size, mode='same')

        plt.scatter(timestamp, signal, s=10, label = 'z')

        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S\n%m/%d'))
        plt.gca().xaxis.set_major_locator(md.AutoDateLocator())
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.grid(color='gray', linestyle=':', linewidth=0.5)
        plt.title(input_file_name)
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Location (m)")
        plt.ylim(-0.5,2)
        plt.tight_layout() 


    # Apply the low-pass filter to center the data for histogram
    cutoff_frequency = 0.5
    sampling_rate = 10
    location_values = locations[:, 1:4]
    data = butter_highpass_filter(np.linalg.norm(location_values, axis=1), cutoff_frequency, sampling_rate)
    x_m = butter_highpass_filter(x_m, cutoff_frequency, sampling_rate)
    y_m = butter_highpass_filter(y_m, cutoff_frequency, sampling_rate)
    z_m = butter_highpass_filter(z_m, cutoff_frequency, sampling_rate)

    threshold = 2 # allowing a variation of 2 meters
    x_m = x_m[x_m > - threshold]
    x_m = x_m[x_m < threshold]
    y_m = y_m[y_m > - threshold]
    y_m = y_m[y_m < threshold]
    z_m = z_m[z_m > - threshold]
    z_m = z_m[z_m < threshold]

    if False:
        plt.scatter(timestamp, x_m, s=8, alpha=0.5, label = 'x')
        plt.scatter(timestamp, y_m, s=8, alpha=0.5, label = 'y')
        plt.scatter(timestamp, z_m, s=8, alpha=0.5, label = 'z')

        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S\n%m/%d'))
        plt.gca().xaxis.set_major_locator(md.AutoDateLocator())
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.grid(color='gray', linestyle=':', linewidth=0.5)
        plt.title(input_file_name)
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Location (m)")
        plt.ylim(-3.5,3.5)
        plt.tight_layout() 

    # Summary statistics for each axis
    if False:
        # plt.figure(figsize=(6, 6))
        plt.hist(x_m, bins=100, alpha=0.5, label='x', color='blue')
        plt.hist(y_m, bins=100, alpha=0.5, label='y', color='orange')
        plt.hist(z_m, bins=100, alpha=0.5, label='z', color='green')
        plt.axhline(y=600, color='r', linestyle='-')
        plt.xlabel('Variance')
        plt.ylabel('Frequency')
        plt.xlim(-0.75, 0.75)
        plt.ylim(0,1000)
        plt.title(input_file_name)
        plt.legend()
        plt.grid(True)

    # Summary statistics with norm
    if False:
        threshold = 10 # allowing a variation of 2 meters
        data = data[data > - threshold]
        data = data[data < threshold]

        variable = data
        summary_stats = {
            # 'Len': len(variable),
            # 'Mean': np.mean(variable),
            'Variance': np.var(variable),
            'STD': np.std(variable),
            # 'Q1': np.percentile(variable, 25),
            # 'Q3': np.percentile(variable, 75),
            # 'IQR=Q3-Q1': np.percentile(variable, 75) - np.percentile(variable, 25),
        }

        # Print summary statistics
        for key, value in summary_stats.items():
            print(f'{key}: {np.round(value,2)}')
        print(" ")

        # plt.figure(figsize=(6, 6))
        plt.hist(data, bins=200, label='norm')
        plt.axhline(y=1000, color='r', linestyle='-')
        plt.xlabel('Variance')
        plt.ylabel('Frequency')
        plt.xlim(-0.75, 0.75)
        plt.ylim(0,1200)
        plt.title(input_file_name)
        plt.legend()
        plt.grid(True)

print("\nDone\n")
plt.show()
