# DairyCows2024


What this is\
This dataset includes two parts: data from wearable sensors and visual data from four cameras.\
Download links:
* [sensor_data.zip](link1) (??GB)
* [single_day_visual_data.zip](link1) (??GB)
* [multi_day_visual_data.zip](link1) (??GB)

<br />
Sensor Data
------

Data from multiple days, from 7/21 to 8/04

**Structure of sensor_data.zip**

```
${ROOT}
|-- measurements 
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
|-- references 
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

<br />
Single-Day Visual Data
------

Data from a single day 7/25\
Annotation rules

**Structure of single_day_visual_data.zip**
```
${ROOT}
|-- images
|-- labels
|-- projection_matrix
|-- visual_location
|-- crop_profiles
```

| Data | Source | Description | Frequency | Duration | Size   |
|-------------|--------|-----------|----------|----------|--------|
| images| Recorded |  | Every 15 s | 1 day  | 20k imgs, 20 GB |
| labels   |images | | Every 15 s | 1 day  | 20k labels |
| projection_matrix |Calibrated|  | N/A| 1 day  |        |
| visual_location | labels (visual) | |Every 15 s | 1 day  |
| crop_profiles| Manual | For masking images | N/A | N/A | |

```1s_interval_images``` that is

<br />

Multi-Day Visual Data
------

Data from multiple days, from 7/21 to 8/04

**Structure of multi_day_visual_data.zip**
```
${ROOT}
|-- images
|-- projection_matrix
|-- crop_profiles
|-- cows_gallery
```

| Data | Source | Frequency | Processing Method | Duration | Size   |
|-------------|--------|-----------|----------|----------|--------|
| images| Recorded | Every 15 s| Aligned | 14 day  |   ? GB     |
| projection_matrix |Calibrated | N/A | Calibrated | 14 days  |        |
| crop_profiles | Manual | N/A | For masking images | N/A | |
| cow_gallery |Captured | N/A | None | N/A  | 500 imgs, 1.92 GB |