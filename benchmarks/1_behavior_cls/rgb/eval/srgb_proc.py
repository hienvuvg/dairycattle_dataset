
import os
import numpy as np

import pytz
from datetime import datetime

import warnings

# Set a global time zone: Central Time
CT_time_zone = pytz.timezone('America/Chicago')

def ratio_to_pixel(disp_resolution, xyn_ratio):
    # down_scale = label_resolution[0]/disp_resolution[0]
    width_loc = int(disp_resolution[0] * xyn_ratio[0])
    height_loc = int(disp_resolution[1] * xyn_ratio[1])
    return width_loc, height_loc

def read_bbox_labels(text_file_dir):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        data_array = np.loadtxt(text_file_dir)
    # print(type(data_array))
    # print(np.shape(data_array))
    return np.atleast_2d(data_array)

def find_behav(dataframe, unix_timestamp):
    # Assuming the dataframe has columns named 'column1' and 'column2'
    result = dataframe[dataframe['timestamp'] == unix_timestamp]['behavior'].values
    if len(result) > 0:
        return result[0]
    else:
        return None  # Or handle the case when the number is not found

def select_range(timestamps, point1, point2):
    assert point1 != point2, f'Invalid range {point2} = {point1}'
    # print(f'{point1} vs {point2}')
    
    if point1 > point2:
        selected = [value for value in timestamps if point2 <= value < point1]
    else:
        selected = [value for value in timestamps if point1 <= value < point2]
    return selected

def srgb_proc(selected_timestamps, id_list, behav_gt_list, pred_label_dir, date, lying = False):
    cow_data = np.empty((0,2)).astype(int)
    for i in range(1,5):
        cam_name = f"cam_{i:d}"
        # folder_path = os.path.join(pred_label_dir, date, cam_name)
        # print(folder_path)
        # filename_list = search_files(folder_path, search_text='_', file_format=".txt")
        for curr_timestamp in selected_timestamps:
            # curr_timestamp = int(single_filename[0:10])
            datetime_var = datetime.fromtimestamp(curr_timestamp, CT_time_zone)
            text_file_name = f'{curr_timestamp:d}_{datetime_var.hour:02d}-{datetime_var.minute:02d}-{datetime_var.second:02d}.txt'
            file_dir = os.path.join(pred_label_dir, date, cam_name, text_file_name)
            try:
                bboxes_data = read_bbox_labels(file_dir)
                if len(bboxes_data.flatten()) > 0:
                    for row in bboxes_data:
                        cow_id = int(row[0])
                        if cow_id in id_list:
                            pred_behav = int(row[5])
                            # cow_name = f'C{cow_id:02d}'
                            test_behav = int(find_behav(behav_gt_list[cow_id-1], curr_timestamp))
                            # if test_behav != pred_behav:
                            #     print(f'{text_file_name}  {cow_name} {test_behav}')
                            if lying == False:
                                if test_behav != 7:
                                    datapoint = np.array([pred_behav, test_behav])
                                    cow_data = np.vstack((cow_data, datapoint))
                            else:
                                datapoint = np.array([pred_behav, test_behav])
                                cow_data = np.vstack((cow_data, datapoint))
            except:
                print('missing', text_file_name)
                pass

    print(np.shape(cow_data))

    y_pred = cow_data[:,0]
    y_test = cow_data[:,1]

    return y_pred, y_test
