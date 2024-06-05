import os
import numpy as np
import pandas as pd
import yaml
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error, r2_score
from math import sqrt
import argparse

# from sklearn.metrics import root_mean_squared_error as root_mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from extract_behav import extract_behav
from avg_thi import get_avg_THI

# Calculate correlation metrics
def calculate_metrics(x, y):
    # Fit the linear regression model
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)
    y_pred = model.predict(x.reshape(-1, 1))

    # Calculate metrics
    r2 = r2_score(y, y_pred)
    # rmse = mean_squared_error(y, y_pred, squared=False)
    rmse = sqrt(mean_squared_error(y, y_pred))
    pearson_corr, p_value = pearsonr(x, y)
    return np.round(r2, 3), np.round(rmse, 3), np.round(pearson_corr, 3), np.round(p_value, 4)

# Function to process data and calculate metrics for different window sizes
def process_data_for_behavior(behav_id, window_sizes, date_list, id_list, daily_THI, pred_behavior_dir):
    best_metrics = {'window_size': None, 'metrics_freq': None, 'metrics_mean_duration': None, 'metrics_total_duration': None}
    best_r2 = -np.inf
    
    for window_size in window_sizes:
        combined_data = extract_behav(pred_behavior_dir, date_list, id_list, window_size, behav_id)

        all_freq_data = []
        all_mean_duration = []
        all_total_duration = []
        all_time_list = []

        for cow_data_dict in combined_data:
            time_list = cow_data_dict['date']
            all_time_list.append(time_list)
            freq_data = cow_data_dict['freq_data']
            mean_duration = cow_data_dict['mean_duration']
            total_duration = cow_data_dict['total_duration']

            all_freq_data.append(freq_data)
            all_mean_duration.append(mean_duration)
            all_total_duration.append(total_duration)

        # Calculate average across all cows
        avg_freq_data = np.mean(all_freq_data, axis=0)
        avg_mean_duration = np.mean(all_mean_duration, axis=0)
        avg_total_duration = np.mean(all_total_duration, axis=0)

        # Ensure lengths match
        if len(avg_freq_data) != len(daily_THI):
            continue
        if len(avg_mean_duration) != len(daily_THI):
            continue
        if len(avg_total_duration) != len(daily_THI):
            continue

        metrics_freq = calculate_metrics(avg_freq_data, daily_THI)
        metrics_mean_duration = calculate_metrics(avg_mean_duration, daily_THI)
        metrics_total_duration = calculate_metrics(avg_total_duration, daily_THI)
        
        # Check if current r2 is the best
        if metrics_freq[0] > best_r2:
            best_r2 = metrics_freq[0]
            best_metrics = {'window_size': window_size, 'metrics_freq': metrics_freq, 'metrics_mean_duration': metrics_mean_duration, 'metrics_total_duration': metrics_total_duration}
    
    return best_metrics

# ===============================================
""" Main program from here """
if __name__ == '__main__':

    current_dir = os.path.join(os.path.dirname(__file__))

    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument('--path_dir', type=str, default=os.path.join(current_dir, 'private', "path.yaml")) 
    args = parser.parse_args() 
    
    yaml_dir = args.path_dir

    with open(yaml_dir, 'r') as file:
        file_dirs = yaml.safe_load(file)
    pred_behavior_dir = file_dirs['pred_behavior_dir']
    sensor_data_dir = file_dirs['sensor_data_dir']
    
    date_list = ['0722','0723','0724','0725','0726','0727','0728','0729','0730','0731','0801','0802','0803']
    id_list = range(1,11)

    input_dir = os.path.join(sensor_data_dir, 'environment', 'indoor_condition', 'average.csv')
    THI_timestamps, daily_THI = get_avg_THI(input_dir)

    behavior_names = {2: "standing", 3: "feeding", 6: "drinking", 7: "lying"}
    window_sizes = range(10, 201, 10)  # Testing window sizes from 10 to 100

    print('Correlating...')

    results = []

    for behav_id in [2, 7, 3, 6]:
        best_metrics = process_data_for_behavior(behav_id, window_sizes, date_list, id_list, daily_THI, pred_behavior_dir)
        
        results.append({
            "Behavior": behavior_names[behav_id],
            "Best Window Size": best_metrics['window_size'],
            "Frequency Metrics (R2, RMSE, Pearson, P-value)": best_metrics['metrics_freq'],
            "Mean Duration Metrics (R2, RMSE, Pearson, P-value)": best_metrics['metrics_mean_duration'],
            "Total Duration Metrics (R2, RMSE, Pearson, P-value)": best_metrics['metrics_total_duration']
        })
    
    # Create a DataFrame to display the results
    results_df = pd.DataFrame(results)
    print(results_df)

