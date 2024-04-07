

import datetime as dt
import os
import csv

import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# from sympy.solvers import solve
# from sympy import *

import time
from datetime import datetime

from multiprocessing import Pool
import yaml

# from utils.GD_uwb_loc import localization
from utils.AdapGrad_uwb_loc import localization

# Set NumPy print options to suppress scientific notation
np.set_printoptions(suppress=True, formatter={'float_kind':'{:.3f}'.format})

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

def create_folder(folder_path):
    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # Create the folder if it doesn't exist
        os.makedirs(folder_path)

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

def check_numbers_exist(arr1, arr2):
    return np.all(np.isin(arr1, arr2))


# ===============================================
""" Main program from here """

def main_func(tag_id):

    # time_data = read_text_timestamp(timestamp_file)

    # Specify the search string
    tag_name = f'T{tag_id:02d}'
    print('\nTag: ' + tag_name)

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

    input_path = os.path.join(dataset_dir, "measurements", "uwb_distance", tag_name)
    output_path = os.path.join(dataset_dir, "processed_data", "neck_location_new", tag_name)

    create_folder(output_path) # Creting output folder

    """ Go through the distance data """
    search_text = "_"
    matched_file_names = search_files(input_path, search_text)
    print(f"Matching files with '{search_text}' in the name:")

    for input_file_name in matched_file_names:
        print('File: ' + input_file_name)
        file_path = os.path.join(input_path, input_file_name)

        df = pd.read_csv(file_path) # skip the firt row, otherwise: header = True
        uwb_data = df.to_numpy()

        # Selecting data based on start/stop timestamps
        timestamps = uwb_data[:,0]

        n_row, _ = np.shape(uwb_data)

        # best_distance = np.empty((0, 5+1))
        location_array = np.empty((0, 4))

        idx = 0
        prev_location = np.array([0, 0, 0]).astype(float) # first initial location
        invalid_row = (-1)*np.ones(6)
        gd = localization()

        while idx < n_row:
            data_point = uwb_data[idx: idx + 8, :]

            ##  Check if all eight datapoints have the same timestamp
            timestamp_point = data_point[:, 0].astype(int)
            if  np.all(timestamp_point == timestamp_point[0]) == False:
                print("==> wrong timestamp: " + str(uwb_data[idx:idx+16, 0]))
                break

            data_point_list = []
            for row in data_point:
                distance = row[2]
                if distance < 22:
                    data_point_list.append(row)
                else:
                    invalid_row[0] = row[0]
                    data_point_list.append(invalid_row)
            data_point = np.asarray(data_point_list).reshape((-1, 6))
            
            curr_location_m, loss_value, n_iterations, selected_anchor_ids = gd.localization(prev_location, data_point)
            
            # Extract data from the selected anchors
            ## timestamp	anchor_id	distance_m	n_samples	LOS_probability	RSSI_dBm
            timestamp = data_point[0,0]
            # anchor_ids  = selected_anchor_ids[:, 1].astype(int)
            # distances   = data_point[:, 2].astype(float)
            # n_samples   = data_point[:, 3].astype(int)
            # LOS_proba   = data_point[:, 4].astype(int)

            datet = dt.datetime.fromtimestamp(timestamp)
            # print(str(datet) + "  " + str(curr_location_m) + "\t" + str(np.round(loss_value,1))+ "\t" + str(n_iterations) + "\t" + str(anchor_ids) + "\t" + str(n_samples) + "\t" + str(LOS_proba))
            print(tag_name + ' ' + str(int(timestamp)) + ' ' + str(datet) + "  " + str(curr_location_m) + "  \t" + str(np.round(loss_value,1))+ "\t" + str(n_iterations) + "\t" + str(selected_anchor_ids))

            if np.isnan(n_iterations):
                location_datapoint = np.hstack((timestamp, curr_location_m)) # in nan
            else:
                location_datapoint = np.hstack((timestamp, np.round(curr_location_m[0]*100,1), np.round(curr_location_m[1]*100,1), np.round(curr_location_m[2]*100,1))) # in cm

            location_array = np.vstack((location_array, location_datapoint))

            curr_z = curr_location_m[2]
            if curr_z <= 2 and curr_z >= 0:
                prev_location = curr_location_m
            else:
                prev_location = np.array([0, 0, 0]).astype(float)

            idx += 8 # Move to next timestamp
        
        # Write location data
        if np.any(location_array):
            file_name = (input_file_name[-12:])[:-4] + ".csv" # select last 12, then select all except last four (.csv)
            file_path = os.path.join(output_path, file_name)
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['timestamp','coord_x_cm', 'coord_y_cm', 'coord_z_cm'])
                writer.writerows(location_array)
                print("Saved: " + file_name)



# ===============================================
""" Run the main program in parallel (all tags at once) """   
if __name__ == '__main__':

    tag_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14]
    # tag_list = [1]
    # tag_list = [2, 7]
    # tag_list = [13, 14]
    # tag_list = [1, 2, 3, 4, 5]


    if len(tag_list) > 1:
        pool = Pool(processes=len(tag_list))
        pool.map(main_func, tag_list)

    else:
        for tag_id in tag_list:
            main_func(tag_id)

    print("\nDone\n")
