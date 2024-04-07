

import csv
import datetime as dt
import os
from datetime import datetime
import time

import numpy as np
import pandas as pd
import yaml

def load_directories_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data

from sklearn.cluster import KMeans

def create_folder(folder_dir):
    # Check if the folder already exists
    if not os.path.exists(folder_dir):
        # Create the folder if it doesn't exist
        os.makedirs(folder_dir)

def datetime_to_unix_timestamp(datetime_str):
    datetime_obj = datetime.strptime(datetime_str, ' %Y/%m/%d %H:%M:%S') # Parse the datetime string into a datetime object
    unix_timestamp = int(time.mktime(datetime_obj.timetuple())) # Convert the datetime object to a Unix timestamp
    return unix_timestamp

def classify_lying(accel_y):

    # Clean the data
    # cleaned_data = accel_y[~np.isnan(accel_y)]
    cleaned_data = accel_y
    accel_data_2D = cleaned_data.reshape(-1, 1)

    # KMeans clustering
    kmeans = KMeans(n_clusters=2, n_init=10, random_state=0).fit(accel_data_2D)

    # Compute the threshold
    centroids = kmeans.cluster_centers_
    threshold = np.mean(centroids)

    # lying = 1 - kmeans.labels_ # incorrect

    # Generate ground truth data
    if threshold < 0:
        lying = (accel_y >= threshold).astype(int)
    else:
        lying = (accel_y < threshold).astype(int)

    return lying

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

    tag_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for tag_id in tag_list:
        cow_name = f'C{tag_id:02d}' 
        sensor_name = f'S{tag_id:02d}'
        print(f"Tag: {cow_name} ") 

        input_path = os.path.join(dataset_dir, "measurements", "ankle_acceleration")
        output_path = os.path.join(dataset_dir, "processed_data", "cow_lying")

        # timestamp	accel_x accel_y accel_z
        file_path = os.path.join(input_path, cow_name + '.csv')
        df = pd.read_csv(file_path)
        ankle_data = df.to_numpy()

        timestamps = ankle_data[:,0]
        accel_y = ankle_data[:,2]

        lying = classify_lying(accel_y)

        output_data = np.hstack((timestamps.reshape((-1,1)), lying.reshape((-1,1))))

        create_folder(output_path)
        output_file_name = cow_name + ".csv" 
        output_dir = os.path.join(output_path, output_file_name)

        with open(output_dir, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'lying'])
            writer.writerows(output_data)
            print("Saved " + output_file_name)


