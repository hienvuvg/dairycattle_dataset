

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
        # print(file_name)
        # Check if the file is a text file
        if file_name.endswith(".csv"):
            # Check if the search text is present in the file name
            if search_text in file_name:
                file_names.append(file_name)
    return sorted(file_names)

def get_ankle_lying(input_dir, sensor_id):
    # tag_name = f'T{tag_id:02d}' # Specify the search string
    idx = sensor_id - 1
    cow_name = f'C{sensor_id:02d}' 
    print(cow_name)

    input_file_name = cow_name + '.csv'
    print('File: ' + input_file_name)
    file_path = os.path.join(input_dir, input_file_name)

    df = pd.read_csv(file_path) # skip the firt row, otherwise: header = True

    # Convert Unix timestamps to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

    # Set the timestamp column as the index
    df.set_index('timestamp', inplace=True)

    # Group by day and calculate the percentage of 1 values
    df.index = df.index.tz_localize('UTC').tz_convert('America/Chicago')
    daily_percentage = df.groupby(df.index.date)['lying'].mean() * 24

    # Get representative timestamps for each day
    representative_timestamps = pd.to_datetime(daily_percentage.index)

    return representative_timestamps[1:-1], daily_percentage[1:-1]

# ===============================================
""" Main program from here """
if __name__ == '__main__':

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

    sensor_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # sensor_list = [4]
    # sensor_list = [1, 2, 3, 4]

    for sensor_id in sensor_list:
        cow_name = f'C{sensor_id:02d}' 
        
        input_dir = os.path.join(dataset_dir, 'processed_data', 'cow_lying')
        representative_timestamps, daily_percentage = get_ankle_lying(input_dir, sensor_id)

        # print(representative_timestamps)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(representative_timestamps, daily_percentage, color='skyblue', label='lying duration')

        # sensor_data = df.to_numpy()

        # stand_timest = sensor_data[:,0]
        # standing  = sensor_data[:,1 ]

        # stand_datet = [dt.datetime.fromtimestamp(ts) for ts in stand_timest]

        # plt.figure()
        # plt.plot(stand_datet, standing)

        plt.gca().xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S\n%m/%d'))
        plt.gca().xaxis.set_major_locator(md.AutoDateLocator())
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.grid(color='gray', linestyle=':', linewidth=0.5)
        plt.title(cow_name)
        plt.ylabel('hours')
        plt.ylim([6, 18])
        plt.legend()
        plt.tight_layout() 

    print("\nDone\n")
    plt.show()
