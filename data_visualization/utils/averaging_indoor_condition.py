

import csv
import datetime as dt
import os
from datetime import datetime

import numpy as np
import pandas as pd

from multiprocessing import Pool
import yaml

def load_directories_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data


def create_folder(folder_dir):
    # Check if the folder already exists
    if not os.path.exists(folder_dir):
        # Create the folder if it doesn't exist
        os.makedirs(folder_dir)

def search_files(folder_dir, search_text, file_type):
    file_names = []
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_dir):
        # Check if the file is a text file
        if file_name.endswith(file_type):
            # Check if the search text is present in the file name
            if search_text in file_name:
                file_names.append(file_name)
    return sorted(file_names)

def find_closest_row(scalar, array):
    first_column = array[:, 0]
    
    differences = np.abs(first_column - scalar) # Calculate the absolute differences
    min_index = np.argmin(differences) # Find the index of the minimum difference
    closest_row = array[min_index, :] # Return the corresponding row
    
    return closest_row

def get_avg_indoor_condition():

    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory
    try:
        yaml_file = os.path.join(current_dir, "config.yaml")
        directories = load_directories_from_yaml(yaml_file)
    except:
        current_dir = os.path.dirname(current_dir)   # Get the parent directory (one level up)
        current_dir = os.path.dirname(current_dir) 
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

    # Get average temperature
    array_list = []
    for i in range(6):
        # timestamp temp humi THI
        input_file_dir = os.path.join(dataset_dir, "references", "indoor_condition",f"S{i+1:02d}" +".csv")
        data = pd.read_csv(input_file_dir).values
        array_list.append(data)

    # Combine timestamps and temperatures into a single list of tuples
    combined_data = [(arr[:, 0], arr[:, 1]) for arr in array_list]
    # Find unique timestamps
    unique_timestamps = np.unique(np.concatenate([data[0] for data in combined_data]))

    # Calculate average temperature for each timestamp
    average_temperatures = []
    for timestamp in unique_timestamps:
        temps = []
        for timestamps, temperatures in combined_data:
            if timestamp in timestamps:
                index = np.where(timestamps == timestamp)[0][0]
                temps.append(temperatures[index])
        average_temp = np.mean(temps)
        average_temperatures.append((timestamp, average_temp))

    average_temperatures = np.asarray(average_temperatures)
    temp_data = np.round(average_temperatures,2).reshape((-1,2))


    # Get average humidity
    # Combine timestamps and temperatures into a single list of tuples
    combined_data = [(arr[:, 0], arr[:, 2]) for arr in array_list]
    # Find unique timestamps
    unique_timestamps = np.unique(np.concatenate([data[0] for data in combined_data]))

    # Calculate average temperature for each timestamp
    average_temperatures = []
    for timestamp in unique_timestamps:
        temps = []
        for timestamps, temperatures in combined_data:
            if timestamp in timestamps:
                index = np.where(timestamps == timestamp)[0][0]
                temps.append(temperatures[index])
        average_temp = np.mean(temps)
        average_temperatures.append((timestamp, average_temp))

    average_temperatures = np.asarray(average_temperatures)
    humi_data = np.round(average_temperatures,2).reshape((-1,2))

    # Get average THI
    # Combine timestamps and temperatures into a single list of tuples
    combined_data = [(arr[:, 0], arr[:, 3]) for arr in array_list]
    # Find unique timestamps
    unique_timestamps = np.unique(np.concatenate([data[0] for data in combined_data]))

    # Calculate average temperature for each timestamp
    average_temperatures = []
    for timestamp in unique_timestamps:
        temps = []
        for timestamps, temperatures in combined_data:
            if timestamp in timestamps:
                index = np.where(timestamps == timestamp)[0][0]
                temps.append(temperatures[index])
        average_temp = np.mean(temps)
        average_temperatures.append((timestamp, average_temp))

    average_temperatures = np.asarray(average_temperatures)
    THI_data = np.round(average_temperatures,2).reshape((-1,2))


    indoor_data = np.hstack((temp_data[:,0].reshape((-1,1)), temp_data[:,1].reshape((-1,1)), humi_data[:,1].reshape((-1,1)), THI_data[:,1].reshape((-1,1))))

    return indoor_data

# ===============================================
""" Main program from here """
if __name__ == '__main__':
    

    # THI_data = np.hstack((THI_data[:,0].reshape((-1,1)), average_array.reshape((-1,1))))
    # temp_list = np.asarray(temp_list).reshape((-1,6))

    data = get_avg_indoor_condition()
    print(np.shape(data))

    # # Write data
    # output_folder = current_dir + '/indoor_condition' 
    # create_folder(output_folder) # Creting output folder 
    # output_file_name = "/indoor_average.csv" 
    # output_dir = output_folder + output_file_name
    # with open(output_dir, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['timestamp', 'temperature_F', 'humidity_per', 'THI'])
    #     writer.writerows(indoor_data)
    #     print("Saved " + output_file_name)

    print("\nDone\n")

