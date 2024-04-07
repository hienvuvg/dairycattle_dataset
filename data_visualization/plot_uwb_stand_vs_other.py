

import datetime as dt
import os

import matplotlib
import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import time
from datetime import datetime
import scipy
import yaml

from plot_avg_THI_by_day import get_avg_THI
from plot_ankle_lying_by_day import get_ankle_lying
from utils.pen_model import *

def load_directories_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data

def search_files(folder_path, search_text, file_format=".csv"):
    file_names = []
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        # print(file_name)
        # Check if the file is a text file
        if file_name.endswith(file_format):
            # Check if the search text is present in the file name
            if search_text in file_name:
                file_names.append(file_name)
    return sorted(file_names)

def euler_to_rotation_matrix(roll_rad, pitch_rad, yaw_rad):
    # Rotation matrices
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll_rad), -np.sin(roll_rad)],
                    [0, np.sin(roll_rad), np.cos(roll_rad)]])

    R_y = np.array([[np.cos(pitch_rad), 0, np.sin(pitch_rad)],
                    [0, 1, 0],
                    [-np.sin(pitch_rad), 0, np.cos(pitch_rad)]])

    R_z = np.array([[np.cos(yaw_rad), -np.sin(yaw_rad), 0],
                    [np.sin(yaw_rad), np.cos(yaw_rad), 0],
                    [0, 0, 1]])

    # Total rotation matrix
    R_total = np.dot(R_z, np.dot(R_y, R_x))

    return R_total

def rotate_vector(vector, roll, pitch, yaw):
    R_total = euler_to_rotation_matrix(roll, pitch, yaw)
    result_vector = np.dot(R_total, vector)
    return result_vector

# ===============================================
""" Main program from here """
if __name__ == '__main__':
    current_dir = os.path.join(os.path.dirname(__file__))  # Folder
    project_dir = os.path.dirname(current_dir)   # Get the parent directory (one level up)

    # tag_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    tag_list = [9]

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

    input_dir = os.path.join(dataset_dir, 'references', 'indoor_condition')
    THI_timestamps, daily_THI = get_avg_THI(input_dir)

    # fig, ax1 = plt.subplots(figsize=(10, 6))

    for tag_id in tag_list:

        tag_name = f'T{tag_id:02d}' 
        cow_name = f'C{tag_id:02d}' 
        print(tag_name)

        north_vector = np.array([0, 9, 0]).astype(float)

        input_dir = os.path.join(dataset_dir, 'processed_data', 'cow_lying')
        ankle_standing_timestamps, daily_ankle_lying = get_ankle_lying(input_dir, tag_id)

        loc_dir = os.path.join(dataset_dir, "processed_data", "neck_location", tag_name)
        head_dir = os.path.join(dataset_dir, "processed_data", "head_direction", tag_name)

        search_text = '.'
        matched_file_names = search_files(loc_dir, search_text)
        # print(f"\tMatching csv files with '{search_text}' in the name:")

        # For each day
        if len(matched_file_names) > 0:
            
            time_list = []
            lying_list = []
            feeding_list = []
            standing_list = []
            milking_list = []
            mineral_list = []
            drinking_list = []
            stand_n_feed_list = []

            if len(matched_file_names[1:-1]) != len(daily_ankle_lying):
                print("Number of dates mismatched")
                exit()

            for input_file_name, ankle_lying in zip(matched_file_names[1:-1], daily_ankle_lying):
                print('File: ' + input_file_name)

                loc_path = loc_dir + "/" + input_file_name
                df = pd.read_csv(loc_path) # skip the firt row, otherwise: header = True
                loc_data = df.to_numpy()

                head_path = head_dir + "/" + input_file_name
                df = pd.read_csv(head_path) # skip the firt row, otherwise: header = True
                head_data = df.to_numpy()

                n_samples = len(loc_data[:,0])
                # print(f"n_samples {n_samples}")

                lying = 0
                feeding = 0
                milking = 0
                mineral = 0
                drinking = 0

                for row1, row2 in zip(loc_data,head_data):
                    loc_x, loc_y, loc_z = row1[1:4]
                    roll, pitch, yaw = row2[1:4]
                    relative_angle  = row2[6]

                    if np.isnan(loc_x) == False:
                        if np.abs(loc_y) < 250 and loc_x < 630 and loc_x > -400:
                            # lying += 1
                            pass
                        if loc_y < -640:
                            if loc_x > 950:
                                mineral += 1
                            else:
                                feeding += 1

                        if relative_angle > 12:
                            phi = np.deg2rad(roll)
                            theta = np.deg2rad(pitch)
                            psi = np.deg2rad(yaw)

                            drink = False
                            vector = rotate_vector(north_vector, theta, phi, -psi) * 0.5
                            
                            v_x, v_y, v_z = vector
                            if v_x < (pen_min_x - trough_x/2) or v_x > (pen_max_x - trough_x):
                                if np.abs(v_y) < trough_y/2:
                                    if pitch < -30:
                                        drink = True

                            if loc_x < (pen_min_x + trough_x) or loc_x > (pen_max_x - trough_x*1.5):
                                if np.abs(loc_y) < trough_y/2:
                                    if pitch < -30:
                                        drink = True
                            
                            if drink == True:
                                drinking += 1

                    else:
                        milking += 1
                
                lying = ankle_lying / 24 * n_samples

                # scale = 24
                # standing = n_samples - lying - feeding - milking # by number of uwb samples

                scale = 100
                standing = n_samples - lying - feeding - milking - mineral # by number of uwb samples
                
                lying_duration = (lying / n_samples) * scale 
                feeding_duration = (feeding / n_samples) * scale
                standing_duration = (standing / n_samples) * scale
                milking_duration = (milking / n_samples) * scale
                mineral_duration = (mineral / n_samples) * scale
                drinking_duration = (drinking / n_samples) * scale
                # print(f"lying_duration {lying_duration:.1f}")
                # print(f"feeding_duration {feeding_duration:.1f}")

                time_list.append(dt.datetime.fromtimestamp(sensor_data[0,0]).date())
                lying_list.append(lying_duration)
                feeding_list.append(feeding_duration)
                standing_list.append(standing_duration)
                milking_list.append(milking_duration)
                mineral_list.append(mineral_duration)
                drinking_list.append(drinking_duration)
                stand_n_feed_list.append(standing_duration + feeding_duration)

                # datet = [dt.datetime.fromtimestamp(ts) for ts in timestamps]

            # print(pd.DatetimeIndex(time_list))

            font = {
                # 'family' : 'arial',
                'family' : 'Helvetica',
                'weight' : 'regular',
                'size'   : 13}
            matplotlib.rc('font', **font)
            text_size = 13
            
            # ## First axis ------------------------------------------------------
            # fig, ax1 = plt.subplots(figsize=(10, 6))
            # ax1.set_title(cow_name)
            # ax1.grid(color='gray', linestyle=':', linewidth=0.5)
            # ax1.set_ylabel("Hours")

            # # # ax1.set_ylim([6, 18])

            # # ax1.bar(time_list, standing_list, label = 'standing')
            # # ax1.set_ylim([0, 14])

            # # # ax1.bar(time_list, mineral_list, label = 'licking mineral')
            # # # ax1.set_ylim([0, 1])

            # # # ax1.bar(time_list, drinking_list, label = 'drinking')
            # # # ax1.set_ylim([0, 0.11])

            # # # plt.plot(time_list, milking_list, label = 'milking')
            # # # plt.ylim([0, 2])

            # # # plt.bar(time_list, stand_n_feed_list, label = 'stand n feed')
            # # # ax1.set_ylim([4, 16])
            # # # plt.bar(time_list, stand_n_feed_list, label = 'stand n feed')
            # # # ax1.set_ylim([0, 100])

            # plt.plot(time_list, feeding_list, label = 'feeding')
            # ax1.set_ylim([0, 6])

            
            ## Combined graph --------------------------------------------------
            ## First axis ------------------------------------------------------
            fig, ax1 = plt.subplots(figsize=(6, 4.15))
            # ax1.set_title(cow_name)
            ax1.grid(color='gray', linestyle=':', linewidth=0.5)

            ax1.bar(time_list, standing_list, label = 'standing', color='tab:orange')
            bottom = np.asarray(standing_list)
            ax1.bar(time_list, feeding_list, bottom=bottom, label = 'feeding', color='tab:blue')
            bottom += np.asarray(feeding_list)
            ax1.bar(time_list, mineral_list, bottom=bottom, label = 'licking', color='darkred')
            bottom += np.asarray(mineral_list)
            ax1.bar(time_list, milking_list, bottom=bottom, label = 'milking', color='y')
            bottom += np.asarray(milking_list)
            ax1.bar(time_list, lying_list, bottom=bottom, label = 'lying', color='tab:green')
            
            ax1.set_ylabel("Percentage (%)", size=text_size)

            ## Second axis -----------------------------------------------------
            ax2 = ax1.twinx()
            ax2.plot(THI_timestamps, daily_THI, color='red', linestyle='-', linewidth=3.5, label='avg THI')
            ax2.set_ylim([55,95])
            # ax1.set_ylabel("deg C")
            # plt.legend()

            # plt.legend()
            ax1.set_xlabel("Date", size=text_size)
            ax2.set_ylabel("THI", size=text_size)
            # plt.tight_layout() 

            # Combine legends for both y-axes
            lines, labels = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax2.legend(lines + lines2, labels + labels2, loc="upper right", ncol=2)

            # ax2.xticks(['7/22','7/24','7/26','7/28','7/30','8/01','8/03'])
            # plt.xticks(rotation=45)  # Rotate x-axis labels: not working
            plt.gca().xaxis.set_major_formatter(md.DateFormatter('%-m/%d'))
            plt.gca().xaxis.set_major_locator(md.DayLocator(interval=2))
            # plt.grid(color='gray', linestyle=':', linewidth=0.5)

            plt.setp( ax1.xaxis.get_majorticklabels(), rotation=30 )

            plt.tight_layout()

            # output_path = os.path.join(current_dir, 'combined_behaviors.pdf')
            # plt.savefig(output_path, transparent=True)

            standing_list = np.asarray(standing_list)

            # x = np.array([1, 2, 3, 4, 5 ])
            # y = np.array([11, 12, 13, 14, 15 ])
            
            slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(standing_list, daily_THI)
            print(f" cow #{tag_id}, r_value: {r_value:.2f}")

    #     plt.plot(time_list, mineral_list, label=cow_name)

    # plt.gca().xaxis.set_major_formatter(md.DateFormatter('%m/%d'))
    # plt.gca().xaxis.set_major_locator(md.AutoDateLocator())
    # # plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    # plt.grid(color='gray', linestyle=':', linewidth=0.5)
    # plt.title(cow_name)
    # plt.legend()
    # plt.xlabel("Day")
    # plt.ylabel("Hour")
    # plt.tight_layout() 


    print("\nDone\n")
    plt.show()
