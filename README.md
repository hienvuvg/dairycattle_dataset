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
|   |-- ankle_accel
|   |-- device_temp
|-- processed_data
|   |-- neck_location
|   |-- neck_elevation
|   |-- head_direction
|   |-- cow_lying
|-- references 
|   |-- body_temp
|   |-- milk_production
|   |-- health_information
|   |-- indoor_condition
|   |-- outdoor_weather
|--behavior_labels
    |-- individual
    |-- social

```
**Text**\
Explaining what each folder contains.

**Text**\
The table of data size and info.

| Data | Source | Description | Frequency| Duration | Size   |
|-------------|--------|-----------|----------|----------|--------|
| ```uwb_distance```| Measured | Distance from the tag to the anchors | Every 15 s  | 14 days  |  0.3GB   |
| ```neck_data```   | Measured | Acceleration, magnetic, and pessure recorded by the neck tags | 10Hz | 14 days  | 9.6GB |
| ```ankle_accel```| Measured | Ankle acceleration from ankle sensors |Every 1 m  | 14 days  |   6MB    |
|```dev_temp```| Measured | Temperature of neck tags |Every 15 s | 14 days  |  19 MB |
|```neck_location```|```uwb_distance```| 3D neck location of the cows | Every 15 s|14 days  |  30MB   |
|```neck_elevation```|Neck pressure| ?? | 10 Hz | 14 days | ?|
|```head_direction```|Neck accel & mag| Tilt-compensated eCompass | 1 Hz|14 days| 0.7GB |
|```cow_lying``` | ```ankle_accel``` | K-mean clustering | Every 1 m | 14 days | 4MB |
|```body_temp```  | Measured | Calibrated  | Every 1 m    | 14 days | 4MB |
|```milk_production```   | Barn staffs | None  | Daily  | 14 days | 10KB | 
|```health_info```| Barn staffs | None  | Periodically | 14 days | 0.2MB |
|```indoor_condition```  | Measured | Calibrated | Every 1 m | 14 days | 4MB |
|```outdoor_weather```   | Weather station | None | Every 3 m    | 14 days | 9MB |
|```individual```| Visual data | Manually created behaviors of individual cows  | 1 Hz| 1 day | 32MB |
|```social```| Visual data | Manually created bunching behavior | 1 Hz | 1 day | 32MB |

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
| ```images```| Recorded | 20k UWB-synchronized 15s-interval images where the other pens with unrelated cows are masked out | Every 15 s | 1 day  | 20GB |
| ```labels```   |Annotated | bbox position with cow_id of each cow in the camera views. Format in image ratio ```[x_center, y_center, width, height]``` | Every 15 s | 1 day  |  |
| ```proj_mat``` |Calibrated| Matrices for projecting a 3D world coordinate to a pixel location in each camera view | N/A| 1 day  |  N/A   |
| ```visual_location``` | ```labels``` (visual) | 3D location of each cow's body computed from the bboxes in 4 camera views using AdaGrad |Every 15 s | 1 day  |
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

| Data | Source | Description | Frequency | Duration | Size   |
|-------------|--------|-----------|----------|----------|--------|
| ```images```| Recorded| 14x20k UWB-synchronized 15s-interval images | Every 15 s | 14 day  |   21GB / zip |
| ```proj_mat``` |Calibrated | Calibrated | N/A | 14 days  | N/A       |
| ```crop_profiles``` | Manual | Pixel locations in each camera view for masking images | N/A | N/A | N/A |
| ```cow_gallery``` |Captured | 500 photos of the cows taken from different angles using phone cameras | N/A | N/A  | 2GB |


**Other sets of visual data:**
* [15s_interval_images](link6) (4.5k resolution, 14 days, 14 zips, 21GB/zip): 
* [1s_interval_videos](link4) (4.5k resolution, 14 day, 14 videos, ?? GB/video) (319GB/zip):  
* [1s_interval_combined_view_videos](link5) (4k resolution, 14 days): Combined view from four cameras, 14 days, 14 videos, 37 GB/video.
