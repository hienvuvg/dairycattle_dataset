

import datetime as dt
import os

import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import time
from datetime import datetime
import yaml

def load_directories_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data

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
if __name__ == '__main__':

    # tag_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14]
    tag_list = [9]
    date = "0725"

    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory
    try:
        yaml_file = os.path.join(current_dir, "config.yaml")
        directories = load_directories_from_yaml(yaml_file)
    except:
        current_dir = os.path.dirname(current_dir)   # Get the parent directory (one level up)
        yaml_file = os.path.join(current_dir, "config.yaml")
        directories = load_directories_from_yaml(yaml_file)

    print("Directories in config.yaml:")
    for key, directory in directories.items():
        print(f"  {key}: {directory}")

        if key == 'dataset':
            dataset_dir = directory 
        if key == 'images':
            image_dir = directory
        if key == 'labels':
            label_dir = directory

    for tag_id in tag_list:

        # for tag_id in tag_list:
        tag_name = f'T{tag_id:02d}' 
        print('\nTag: ' + tag_name)
        cow_name = f'C{tag_id:02d}'

        input_file_name = tag_name + '_' + date + ".csv"
        # available_file_names = search_files(input_path, "location_data")

        print('File: ' + input_file_name)
        file_path = os.path.join(dataset_dir, 'processed_data', 'neck_location', tag_name, input_file_name)
        # file_path = os.path.join(dataset_dir, 'processed_data', 'neck_location_new', tag_name, input_file_name)

        df = pd.read_csv(file_path) # skip the firt row, otherwise: header = True
        data = df.to_numpy()


        timestamps = data[:,0]
        locations = data[:,1:4]

        plt.figure()

        """ Ploting location data """ 

        x_m = locations[:,0]/100
        y_m = locations[:,1]/100
        z_m = locations[:,2]/100

        timestamp = [dt.datetime.fromtimestamp(ts) for ts in timestamps]

        # plt.scatter(timestamp, x_m, s=3, label = 'x', alpha=0.8)
        # plt.scatter(timestamp, y_m, s=3, label = 'y', alpha=0.8)
        plt.scatter(timestamp, z_m, s=3, label = 'z', alpha=0.8)

        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S\n%m/%d'))
        plt.gca().xaxis.set_major_locator(md.AutoDateLocator())
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.grid(color='gray', linestyle=':', linewidth=0.5)
        plt.title('\nTag: ' + tag_name + ' ' + input_file_name)
        plt.legend()
        plt.xlabel("Time")
        plt.ylabel("Location (m)")
        plt.ylim(-12,12)
        # plt.ylim(-1,3)

        # """ Ploting ankle data """
        # plot_ankle = 1
        # if plot_ankle == 1:
        #     # Get standing reference
        #     try:
        #         input_file_dir = project_dir + "/CPS_cow_data_v1/standing_reference/" + cow_name + '/' + cow_name + "_" + date + ".csv"
        #         ref_data = pd.read_csv(input_file_dir).values[:,0:2].astype(int)
        #         standing_timestamps = ref_data[:,0]
        #         standing = ref_data[:,1]

        #         datet = [dt.datetime.fromtimestamp(ts) for ts in standing_timestamps]
        #         plt.plot(datet, standing, color='orange', label='standing')

        #     except:
        #         print("No standing reference")

        # plt.tight_layout() 

    print("\nDone\n")
    plt.show()
