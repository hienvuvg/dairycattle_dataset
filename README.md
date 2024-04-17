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

| Data | Source | Frequency | Processing Method | Duration | Size   |
|-------------|--------|-----------|----------|----------|--------|
| uwb_distance| Measured | Every 15 s| Calibrated  | 14 days  |        |
| neck_data   | Measured | 10 Hz     | Calibrated | 14 days  | 9.6 GB |
| ankle_acceleration| Measured |Every 1 m|Calibrated  | 14 days  |        |
|device_temperature| Measured |Every 15 s|Calibrated | 14 days  |        |
|neck_location|uwb_distance|Every 15 s|Adaptive Gradient|14 days  |        |
|neck_elevation|Neck pressure| 10 Hz | ?? | 14 days |
|head_direction|Neck accel & mag| 1 Hz | Tilt-compensated eCompass|14 days| |
|cow_lying | ankle_acceleration | Every 1 m | K-mean clustering | 14 days | |
|body_temperature  | Measured | Every 1 m  | Calibrated    | 14 days | |
|milk_production   | Barn staffs | Daily | None  | 14 days | | 
|health_information| Barn staffs | Log   | None  | 14 days | |
|indoor_condition  | Measured | Every 1 m  | Calibrated    | 14 days | |
|outdoor_weather   | Weather station | Every 3 m | None    | 14 days | |
|individual_behaviors| Visual data | 1 Hz | Manually created | 1 day | |
|bunching_behavior| Visual data | 1 Hz | Manually created | 1 day | |


Visual Data
------
**Structure of visual_data.zip**
```
${ROOT}
|-- images
|-- labels
|-- visual_location
|-- projection_matrix
|-- crop_profiles
|-- cows_gallery
```

| Data | Source | Frequency | Processing Method | Duration | Size   |
|-------------|--------|-----------|----------|----------|--------|
| images| Recorded    | Every 15 s| Calibrated  | 1 day  |   ? GB     |
| labels   | Annotated |Every 15 s|  | 1 day  |  |
| projection_matrix |Calibrated |  | 14 days  |        |
| visual_location |Raw|Every 15 s| Adaptive Gradient | 1 day  |        |
| cow_gallery |Captured | N/A | None | N/A  |        |


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