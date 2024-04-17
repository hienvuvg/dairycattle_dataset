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
|   |-- indoor_condition
|   |-- outdoor_weather
|   |-- body_temperature
|   |-- milk_log
|   |-- health_information
|--behavior_labels
    |-- individual_behaviors
    |-- bunching_behavior

```
**Text**\
Explaining what each folder contains.

**Text**\
The table of data size and info.

| Sensor Data | Source | Frequency | Processing Method | Duration | Size |
|-------------|--------|-----------|-------------------|----------|------|
| uwb_distance| 30  | Engineer   |
| Bob   | 25  | Designer   |
| Carol | 35  | Teacher    |


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