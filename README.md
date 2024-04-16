# DairyCows2024



Text
------

*   Text



**Directory of the sensor data**

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
|   |-- cow_resting
|-- annotated_behaviors
|   |-- (standing/resting/...)
|-- references (raw)
|   |-- indoor_condition
|   |-- outdoor_weather
|   |-- body_temperature
|   |-- milk_log
|   |-- health_information

```

**Directory of the visual data**
```
${ROOT}
|-- isometric_images
|   |-- 0725.zip (MMDD)
|   |-- sensor_data
|   |-- head_direction
|   |-- device_temperature
|-- calibration (projection matrix)
|   |-- 0725
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