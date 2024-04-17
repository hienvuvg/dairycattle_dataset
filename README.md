# DairyCows2024


What this is\
This dataset includes two parts: data from wearable sensors and visual data from four cameras.\
**Download links:**
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

| Data | Source | Description | Frequency| Duration | Size   |
|-------------|--------|-----------|----------|----------|--------|
| ```uwb_distance```| Measured | Calibrated | Every 15 s  | 14 days  |  288 MB   |
| ```neck_data```   | Measured | Calibrated  | 10 Hz | 14 days  | 9.6 GB |
| ```ankle_acceleration```| Measured | Calibrated |Every 1 m  | 14 days  |   6 MB    |
|```device_temperature```| Measured | Calibrated |Every 15 s | 14 days  |  19 MB |
|```neck_location```|uwb_distance|Adaptive Gradient | Every 15 s|14 days  |  30 MB   |
|```neck_elevation```|Neck pressure| ?? | 10 Hz | 14 days | ?|
|```head_direction```|Neck accel & mag| Tilt-compensated eCompass | 1 Hz|14 days| 686 MB |
|```cow_lying``` | ankle_acceleration | K-mean clustering | Every 1 m | 14 days | 4 MB |
|```body_temperature```  | Measured | Calibrated  | Every 1 m    | 14 days | 4 MB |
|```milk_production```   | Barn staffs | None  | Daily  | 14 days | 10 KB | 
|```health_information```| Barn staffs | None  | Periodically | 14 days | 0.2 MB |
|```indoor_condition```  | Measured | Calibrated | Every 1 m | 14 days | 4 MB |
|```outdoor_weather```   | Weather station | None | Every 3 m    | 14 days | 9 MB |
|```individual_behaviors```| Visual data | Manually created  | 1 Hz| 1 day | 32 MB |
|```bunching_behavior```| Visual data | Manually created | 1 Hz | 1 day | 32 MB |

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
|-- proj_mat
|-- visual_location
|-- crop_profiles
```

| Data | Source | Description | Frequency | Duration | Size   |
|-------------|--------|-----------|----------|----------|--------|
| ```images```| Recorded | UWB-synchronized 15s-interval images where the other pens with unrelated cows are masked out | Every 15 s | 1 day  | 20k imgs, 20 GB |
| ```labels```   |images | bbox position with cow_id of each cow in the camera views. Format in image ratio ```[x_center, y_center, width, height]``` | Every 15 s | 1 day  | 20k labels |
| ```proj_mat``` |Calibrated| Matrices for projecting a 3D world coordinate to a pixel location in each camera view | N/A| 1 day  |  N/A   |
| ```visual_location``` | labels (visual) | 3D location of each cow's body computed from the bboxes in 4 camera views using AdaGrad |Every 15 s | 1 day  |
| ```crop_profiles```| Manual | Pixel locations in each camera view for masking images | N/A | N/A | N/A |

[1s_interval_images.zip](link3) that is

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
| ```images```| Recorded | Every 15 s| Aligned | 14 day  |   ? GB     |
| ```proj_mat``` |Calibrated | N/A | Calibrated | 14 days  | N/A       |
| ```crop_profiles``` | Manual | N/A | Pixel locations in each camera view for masking images | N/A | N/A |
| ```cow_gallery``` |Captured | N/A | 500 photos of the cows taken from different angles using phone cameras | N/A  | 1.92 GB |


**Other sets of visual data:**
* [15s_interval_images](link6) (4.5k resolution, 14 days, 14 zips, 21GB/zip): 
* [1s_interval_videos](link4) (4.5k resolution, 14 day, 14 videos, ?? GB/video) (319GB/zip):  
* [1s_interval_combined_view_videos](link5) (4k resolution, 14 days): Combined view from four cameras, 14 days, 14 videos, 37 GB/video.
