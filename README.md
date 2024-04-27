# DairyCows2024


What this is\
This dataset includes two parts: data from wearable sensors and visual data from four cameras.\
[Overview](https://hienvuvg.github.io/dairycattle_dataset/)\
**Download links:**
* [sensor_data.zip](link1) (11GB)
* Aligned visual data is provided in multiple mp4 and zip files
* [annotated_visual_data.zip](link1) (29GB)

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
|   |-- UWB_location
|   |-- neck_elevation
|   |-- head_direction
|   |-- cow_lying
|   |-- visual_location
|--behavior_labels
|   |-- individual
|   |-- social
|-- references 
    |-- body_temp
    |-- milk_production
    |-- health_information
    |-- indoor_condition
    |-- outdoor_weather


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
|```UWB_location```|```uwb_distance```| 3D neck location of the cows | Every 15 s|14 days  |  30MB   |
|```neck_elevation```|Neck pressure| Elevation of the cow relative to the sea level | 10 Hz | 14 days | 3 GB|
|```head_direction```|Neck accel & mag| Head direction calculated using Tilt-compensated eCompass | 10 Hz|14 days| 5.2GB |
|```cow_lying``` | ```ankle_accel``` | Cow's lying behavior calculated from the ankle acceleration using K-mean clustering | Every 1 m | 14 days | 4MB |
|```visual_location``` | visual ID annotation | Cow's 3D body location computed from the annotated data using optimization-based localization | Every 15 s | 1 day | ??MB |
|```individual```| Visual data | Manually created behaviors of individual cows  | 1 Hz| 1 day | 32MB |
|```social```| Visual data | Manually created bunching behavior | 1 Hz | 1 day | 32MB |
|```body_temp```  | Measured | Body temperature measured by the varginal temperature sensor | Every 1 m    | 14 days | 4MB |
|```milk_production```   | Barn staffs | Daily milk yield of each cow in kg | Daily  | 14 days | 10KB | 
|```health_info```| Barn staffs | Health information of the cows | Periodically | 14 days | 0.2MB |
|```indoor_condition```  | Measured | Temperature and humidity around the pen | Every 1 m | 14 days | 4MB |
|```outdoor_weather```   | Weather station |  Outdoor weather collected by a near by weather station | Every 3 m    | 14 days | 9MB |

<br />

Aligned Visual Data
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

| Data | Source | Description | Interval | Duration | Size   |
|-------------|--------|-----------|----------|----------|--------|
| ```images```| Recorded| 14x20k UWB-synchronized 15s-interval images | Every 15 s | 14 day  |   21GB / zip |
| ```proj_mat``` |Calibrated | Matrices for projecting a 3D world coordinate to a pixel location in each camera view | N/A | 14 days  | N/A       |
| ```crop_profiles``` | Manual | Pixel locations in each camera view for masking images | N/A | N/A | N/A |
| ```cow_gallery``` |Captured | 500 photos of the cows taken from different angles using phone cameras | N/A | N/A  | 2GB |


**Multiple sets of visual data:**
* ```15s_interval_images``` (4.5k resolution, 14 days, 14 zips, 20k images/zip, 21GB/zip): 
* ```1s_interval_videos``` (4.5k resolution, 14 day, 14x4 videos, 40GB/video, 120 GB/ 4 videos) (319GB/zip):  
* ```1s_interval_combined_view_videos``` (4k resolution, 14 days): Combined view from four cameras, 14 days, 14 videos, 37 GB/video.


<br />

Annotated Visual Data
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

| Data | Source | Description | Interval | Duration | Size   |
|-------------|--------|-----------|----------|----------|--------|
| ```images```| Recorded | 20k UWB-synchronized 15s-interval images where the other pens with unrelated cows are masked out | Every 15 s | 1 day  | 20GB |
| ```labels```   |Annotated | bbox position with cow_id of each cow in the camera views. Format in image ratio ```[x_center, y_center, width, height]``` | Every 15 s | 1 day  |  |
| ```proj_mat``` |Calibrated| Matrices for projecting a 3D world coordinate to a pixel location in each camera view | N/A| 1 day  |  N/A   |
| ```visual_location``` | ```labels``` (visual) | 3D location of each cow's body computed from the bboxes in 4 camera views using AdaGrad |Every 15 s | 1 day  |
| ```crop_profiles```| Manual | Pixel locations in each camera view for masking images | N/A | N/A | N/A |

[1s_interval_images.zip](link3) that is



<br />

Annotation Rules for Visual Data
------
**Isometric-view cow identification:** \

| # | Text | Text |
|-------------|--------|-----------|
| 0 | Text | Text | N/A |


**Cow behaviors for behavior labels:** \

| # | Behavior | Definition |
|-------------|--------|-----------|
| 0 | Unknow | When the cow is absent or the light is off | N/A |
| 1 | Walking | Moving from one location to another between consecutive frames |  |
| 2 | Standing | The legs are straight up for supporting the body and the head is not at the feeding area | |
| 3 | Feeding head up | The head is at the feeding area and the mouth is above the food | |
| 4 | Feeding head down | The head is at the feeding area and the mouth touches the food | |
| 5 | Licking | Licking the mineral block | |
| 6 | Drinking | Drinking at the water trough, when the mouth touches the water | |
| 7 | Lying | The cow lies in the stall |<!--<img src="docs/imgs/bunching.png" style="max-width:100%; height:auto;" />-->|
| 8 | Bunching | When there are at least three cows standing right next to each other including the current cow, excluding standing in the stall, feeding, licking, and drinking |<!--![](docs/imgs/bunching.png)--> |

Visual examples of the behaviors are provided in ```x.docx``` which is included in the zip.