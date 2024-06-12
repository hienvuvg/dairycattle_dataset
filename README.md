# MmCows


<!--What this is\-->
This dataset includes two parts: data from wearable sensors and visual data from four cameras.\
[Overview](https://hienvuvg.github.io/mmcows/)\
**Download links:**
* [sensor_data.zip](https://www.dropbox.com/scl/fi/k2qikwjw8lamm5u8w8m76/sensor_data.zip?rlkey=x897xeha714nsd0m16tphqbyb&dl=1) (18 GB) Data from wearable sensors
* [visual_data.zip](https://www.dropbox.com/scl/fi/yiw5khfkzizntooz2if5y/visual_data.zip?rlkey=ncpvn9hn3kh9dbriykacthexy&dl=1) (23 GB) 15s interval visual data of 7/25
* [cropped_bboxes.zip](https://www.dropbox.com/scl/fi/44d79t76i3bm81u3s7dk9/cropped_bboxes.zip?rlkey=needcxkpfw1ujo4i9d4fscb23&dl=1) (13 GB) cropped bounding boxes of cows for the training of behavior classification, lying cow identification, and non-lying cow identification
* Visual data of 14 days with sampling rates of 1s and 15s is provided in multiple mp4 and zip files

<!--* [pred_labels.zip](https://www.dropbox.com/scl/fi/d6wj82bmi5v6whret8wwu/pred_labels.zip?rlkey=srg3cnqou72yfuuxvdu51z7hg&dl=1) (20 MB) Predicted labels from visual models on 7/25-->

<br />

Benchmarks
------
**Benchmarking of UWB-related models:** <br /> 
Setup:
1. Download and upzip ```sensor_data.zip``` and ```visual_data.zip``` to separate folders
2. Clone this directory: 
	```
	git clone https://github.com/hienvuvg/dairycattle_dataset
	```
	In ```./configs/path.yaml```, modify ```sensor_data_dir``` and ```visual_data_dir``` to your local directories of the respective folders
3. [Optional] Create a virtual environment using conda: 
	```
	conda create -n mmcows python=3.9
	conda activate mmcows
	```
4. Install all dependencies using python (3.8 or 3.11, idealy 3.9) before running the test:
	```
	pip install -r requirements.txt
	```
<br />
There are two options for benchmarking the dataset:

A. Test all models using provided weights:
1. Navigate to your local directory of this repo
2. To evaluate the performance of the modalities, run
	```
	sh test_all_moda.sh
	```
1. To show the correlations between cows' behavior changes and THI thoughout the deployment, run
	```
	sh test_behaviors.sh
	```

B. Train and test all models from scratch:
1. Navigate to your local directory of this repo
2. To evaluate the performance of the modalities, run
	```
	sh train_test_all_moda.sh
	```
1. To show the correlations between cows' behavior changes and THI thoughout the deployment, run
	```
	sh train_test_behaviors.sh
	```

Note:
* In the scripts, s1 = OS (object-wise split), s2 = TS (temporal split)


**RGBs and RGBm benchmarking:** <br /> 
* Follow [this readme](https://github.com/hienvuvg/dairycattle_dataset/blob/main/benchmarks/1_behavior_cls/rgb/README.md) for benchmarking RGBs and RGBm.

<br />

<mark>Note: The content below is currently being revisied</mark>
------


Sensor Data
------

Data of 14 days, from 7/21 to 8/04

**Structure of sensor_data.zip**

<!--Old
```
${ROOT}
|-- measurements 
|   |-- uwb_distance
|   |-- neck_data
|   |   |-- acceleration
|   |   |-- magnetic
|   |   |-- pressure
|   |-- ankle_accel
|   |-- cbt
|   |-- milk_yield
|   |-- health_records
|-- processed_data
|   |-- UWB_location
|   |-- head_direction
|   |-- neck_elevation
|   |-- ankle_lying
|   |-- visual_location
|-- behavior_labels
|   |-- individual
|-- environment 
    |-- indoor_condition
    |-- outdoor_weather
```-->


```
${ROOT}
|-- main_data
|   |-- uwb
|   |-- immu
|   |   |-- acceleration
|   |   |-- magnetic
|   |-- pressure
|   |-- cbt
|   |-- ankle
|   |-- thi
|   |-- weather
|   |-- milk
|-- sub_data
|   |-- head_direction
|   |-- uwb_distance
|   |-- ankle_accel
|   |-- visual_location
|   |-- health_records
|-- behavior_labels
    |-- individual
```

**Text**\
Explaining what each folder contains.

**Text**\
The table of data size and info.

| Data  | Description | Frequency| Duration    |
|-------------|-----------|----------|----------|
| ```uwb``` | 3D neck location of the cows | Every 15 s  | 14 days    |
| ```pressure``` | Ambient air pressure at the cow neck | 10 Hz  | 14 days    |
| ```uwb_distance``` | Distance from the tag to the anchors | Every 15 s  | 14 days    |
| ```immu```    | Acceleration, magnetic, and pessure recorded by the neck tags | 10Hz | 14 days   |
| ```ankle_accel``` | Ankle acceleration from ankle sensors |Every 1 m  | 14 days   |
|```head_direction```| Head direction calculated using tilt-compensated eCompass | 10 Hz|14 days| 
|```ankle_lying``` | Cow's lying behavior calculated from the ankle acceleration using K-mean clustering | Every 1 m | 14 days | 
|```visual_location``` | Cow's 3D body location computed from the annotated data using optimization-based localization | Every 15 s | 1 day | 
|```individual```| Manually annotated individual behaviors of the cows  | 1 Hz| 1 day | 
|```cbt```   | Core body temperature measured by the varginal temperature sensor | Every 1 m    | 14 days |
|```milk_production```    | Daily milk yield of each cow in kg | Daily  | 14 days | 
|```health_info``` | Health information of the cows | Periodically | 14 days | 
|```indoor_condition```  | Temperature and humidity around the pen | Every 1 m | 14 days | 
|```outdoor_weather```  |  Outdoor weather collected by a near by weather station | Every 3 m    | 14 days | 

Vision-related and manually annotated data is available for all 16 cows while data from wearable sensors is available for cow #1 to #10.


Time index format is unix timestamp. When converting unix timestamp to datetime, it needs to be converted to Central Daylight Time (CDT) which is 5 hours off from the Coordinated Universal Time (UTC).


 


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
|   |-- standing
|   |-- lying
|   |-- combined
|-- proj_mat
|-- visual_location
|-- crop_profiles
```

| Data  | Description | Interval | Duration    |
|-------------|-----------|----------|----------|
| ```images``` | 20k UWB-synchronized 15s-interval images where the other pens with unrelated cows are masked out | 15 s | 1 day   |
| ```labels```    | bbox position with cow_id of each cow in the camera views, formated in image ratio ```[x,y,w,h]```, separated in three sets: standing cows only, lying cow only, or both standing and lying cows | 15 s | 1 day  | 
| ```proj_mat``` | Matrices for projecting a 3D world coordinate to a pixel location in each camera view | N/A| 1 day   |
| ```visual_location``` | 3D location of each cow's body computed from the bboxes in 4 camera views using AdaGrad | 15 s | 1 day  |
| ```crop_profiles``` | Pixel locations in each camera view for masking images | N/A | N/A  |

[1s_interval_images.zip](link3) that is

<br />

UWB-Synced Visual Data (15s interval)
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

| Data  | Description | Interval | Duration    |
|-------------|-----------|-----------|----------|
| ```images```| 14x20k UWB-synchronized 15s-interval images | 15 s | 14 day  |  
| ```proj_mat```  | Matrices for projecting a 3D world coordinate to a pixel location in each camera view | N/A | 14 days  |
| ```crop_profiles```  | Pixel locations in each camera view fr masking images | N/A | N/A | 
| ```cow_gallery```  | 500 photos of the cows taken from different angles using phone cameras | N/A | N/A  |


**Multiple sets of visual data:**
* ```15s_interval_images``` (4.5k resolution, 14 days, 14 zips, 20k images/zip, 21GB/zip): 
* ```1s_interval_videos``` (4.5k resolution, 14 day, 14x4 videos, 40GB/video, 120 GB/ 4 videos) (319GB/zip):  
* ```1s_interval_combined_view_videos``` (4k resolution, 14 days): Combined view from four cameras, 14 days, 14 videos, 37 GB/video.


<br />

Complete Visual Data (1s interval)
------


<br />

Annotation Rules for Visual Data
------
**Isometric-view cow identification:** 

| # | Text | Text |
|-------------|--------|-----------|
| 0 | Text | Text | N/A |


**Cow behaviors for behavior labels:** 

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

<!--| 8 | Bunching | When there are at least three cows standing right next to each other including the current cow, excluding standing in the stall, feeding, licking, and drinking |<!--![](docs/imgs/bunching.png)--> |-->

Visual examples of the behaviors are provided in ```x.docx``` which is included in the zip.
