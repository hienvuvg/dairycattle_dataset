# Data Visualization



## Setup
* Specify file directories in ```path.yaml``` to the two unzipped folders.
* Install all dependencies using python before running the scripts:
	```
	cd visualization
	pip install -r requirements.txt
	```
<br />

## MmCows Viewer
For showing the 3D map of the pen with UWB location and a combined camera view which is time-synchronized with the map:

```
python MmCows_view.py
```

For visualizing the isometric-view images along with the sensor data, download the zipped images of the day-of-interest and the projection matrices (proj_mat.zip) from [this folder](https://purdue0-my.sharepoint.com/:f:/g/personal/vu64_purdue_edu/Et4vQrsbOvRNudWe7SGn7p0BzPJlyWY6jXG1NOn39me5-A?e=DuY0TM) (completed UWB-synced frames, 24 hours for each day). Then unzip and organize them in the ```visual_data``` folder as the following structure:
```
${ROOT}
|-- images
|   |-- 0721
|   |   |-- cam_1
|   |   |-- cam_2
|   |   |-- cam_3
|   |   |-- cam_4
|   |-- 0722
|   |-- 0723
|   |-- ...
|   |-- 0803
|   |-- 0804
|-- proj_mat
    |-- 0721
    |-- ...
    |-- 0803
    |-- 0804
```
Note: The annotated ```visual_data.zip``` only contains images on 7/25 from 2:57:18 to 23:57:17 which are also already masked. Refer to the link above for the original UWB-synced unmaked 24-hour frames.


There are several flags for passing into the python script that allow visualization of different parameters in the image views:
* ```--date```, specifying the chosen date to be visualized in MMDD
* ```--no_image```, disabling the second window that displays the images
* ```--uwb_points```, showing 3D UWB locations in the camera views
* ```--bbox```, drawing bounding boxes from the cow ID labels (only applicable on 7/25)
* ```--ground_grid```, showing the ground grid and the pen boundary in the camera views
* ```--boundary```, showing the pen boundary in the camera views
* ```--disp_intv```, set display interval of the animation
* ```--freeze```, stop the annimation at run


Example:

```
python MmCows_view.py --date 0725 --uwb_points --boundary
```


https://github.com/hienvuvg/dairycattle_dataset/assets/60267498/905ce915-ac74-4938-a492-9a556bbe61b5

<br />

## UWB Localization
Localization of a single cow using UWB:
```
python uwb_localization.py
```


https://github.com/hienvuvg/dairycattle_dataset/assets/60267498/8d7f469a-cf4c-4224-b486-c96c0a1ab6e1

<br />

## Multi-View Visual Localization
Localization of cows (from 1 to 16) simultaneously using multiple views. Only applicable to 7/25:
```
python visual_localization.py
```

https://github.com/hienvuvg/dairycattle_dataset/assets/60267498/adf83598-4eef-40a0-a9d5-57c1a96f41de


If you cannot see the videos, hold the "shift" key while refreshing your browser to reload the page.