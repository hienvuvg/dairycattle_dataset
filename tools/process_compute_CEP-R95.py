

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


def compute_cep_r95(locations):
    # Exclude np.nan values from the locations
    locations = locations[~np.isnan(locations).any(axis=1)]

    # Compute the mean position
    mean_position = np.mean(locations, axis=0)

    # Calculate distances from each point to the mean position
    distances = np.linalg.norm(locations - mean_position, axis=1)

    # Sort the distances
    sorted_distances = np.sort(distances)

    # print(f"min {sorted_distances[0]}, max {sorted_distances[-1000]}")

    # Find the index corresponding to the 95th percentile
    index_95_percentile = int(0.95 * len(sorted_distances))

    # Circular Error Probability (CEP-R95) is the distance at the 95th percentile
    cep_r95 = sorted_distances[index_95_percentile]

    return cep_r95

# ===============================================
""" Main program from here """
if __name__ == '__main__':

    tag_list = [13, 14]
    list_of_dates = ["0721", "0722", "0723", "0724","0725","0726","0727","0728","0729","0730","0731","0801","0802","0803","0804"]

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
        locations = np.empty((0,3))

        for date in list_of_dates:

            tag_name = f'T{tag_id:02d}' 
            # print(f"Tag: {tag_name} " + date) 

            # Get UWB location data
            # timestmap x_m y_m z_m
            location_data_dir = os.path.join(dataset_dir, 'processed_data', "neck_location", tag_name, tag_name + "_" + date + ".csv")
            # location_data_dir = os.path.join(dataset_dir, 'processed_data', "neck_location_new", tag_name, tag_name + "_" + date + ".csv")
            loc_df = pd.read_csv(location_data_dir)
            day_locations = loc_df[['coord_x_cm', 'coord_y_cm', 'coord_z_cm']].values
            # loc_timestamp = loc_df[['timestamp']].values

            locations = np.vstack((locations, day_locations))

        # print(np.shape(locations))
        print(' ')
        # Compute the Circular Error Probability at the 95% level (CEP-R95)
        cep_r95 = compute_cep_r95(locations)

        print(tag_name + f" CEP-R95: {cep_r95:.2f} cm", )
            


