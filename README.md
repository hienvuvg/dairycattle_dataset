# DairyCows2024


What this is\
This dataset includes two parts: data from wearable sensors and visual data from four cameras.\
Download links:
* [sensor_data.zip](link1) (??GB)
* [visual_data.zip](link1) (??GB)


Sensor Data
------


**Structure of sensor_data.zip**

```
${ROOT}
|-- measurements (raw)
|   |-- uwb_distance
|   |-- neck_data
|   |   |-- acceleration
|   |   |-- magnetic
|   |   |-- pressure
|   |-- ankle_acceleration
|   |-- device_temperature
|-- processed_data
|   |-- neck_location
|   |-- neck_elevation
|   |-- head_direction
|   |-- cow_lying
|-- references (raw)
|   |-- body_temperature
|   |-- milk_production
|   |-- health_information
|   |-- indoor_condition
|   |-- outdoor_weather
|--behavior_labels
    |-- individual_behaviors
    |-- bunching_behavior

```
**Text**\
Explaining what each folder contains.

**Text**\
The table of data size and info.

| Sensor Data | Source | Frequency | Processing Method | Duration | Size   |
|-------------|--------|-----------|-------------------|----------|--------|
| uwb_distance| Raw    | Every 15 s| Calibrated        | 14 days  |        |
| neck_data   | Raw    | 10 Hz     | Calibrated        | 14 days  | 9.6 GB |
| ankle_acceleration|Raw|Every 1 m|Calibrated       | 14 days  |        |
|device_temperature|Raw|Every 15 s|Calibrated          | 14 days  |        |
|neck_location|uwb_distance|Every 15 s|Adaptive Gradient|14 days  |        |
|neck_elevation|Neck pressure| 10 Hz | | 14 days |
|head_direction|Neck accel & mag| 1 Hz | Tilt-compensated eCompass|14 days| |
|cow_lying | ankle_acceleration | Every 1 m | K-mean clustering | 14 days | |
|body_temperature  | Raw | Every 1 m  |     | 14 days | |
|milk_production   | Raw | Daily       |     | 14 days | | 
|health_information| Raw | Log         |     | 14 days | |
|indoor_condition  | Raw | Every 1 m  |     | 14 days | |
|outdoor_weather   | Raw | Every 3 m |     | 14 days | |
|individual_behaviors| Visual data | 1 Hz | Manually created | 1 day | |
|bunching_behavior| Visual data | 1 Hz | Manually created | 1 day | |


Visual Data
------
**Structure of visual_data.zip**
```
${ROOT}
|-- images
|-- labels
|-- body_2D_location
|-- visual_neck_location
|-- projection_matrix
|-- crop_profiles
|-- cows_gallery
```

[abc](abc)

<!--```
${ROOT}
|-- visual_data
|   |-- neck_data
|   |   |-- uwb_distance
|   |   |-- sensor_data
|   |   |-- head_direction
|   |   |-- device_temperature
|   |-- location_data
|   |-- ankle_data
```-->