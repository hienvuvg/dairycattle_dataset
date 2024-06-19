# Data Visualization



**Setup:**
* Specify file directories in ```path.yaml``` to the two unzipped folders.
* Install all dependencies using python before running the test:
	```
	cd visualization
	pip install -r requirements.txt
	```
	
**Tools:**
* ```MmCows_view.py``` shows the 3D map of the pen with UWB location and a combined camera view which is time-synchronized with the map.


Note: Use ```--help``` to show config options.

```
${ROOT}
|-- images
    |-- 0721
    |   |-- cam_1
    |   |-- cam_2
    |   |-- cam_3
    |   |-- cam_4
    |-- 0722
    |-- 0723
    |-- ...
    |-- 0803
    |-- 0804
```
<div align="center">
<video width="800" controls autoplay loop>
  <source src="./files/mmcows_view_vid.mp4" type="video/mp4">
</video>
</div>

* ```uwb_localization.py``` illustrates the localization of a single cow using UWB.

<div align="center">
<video width="800" controls autoplay loop>
  <source src="./files/uwb_loc_vid.mp4" type="video/mp4">
</video>
</div>

* ```visual_localization.py``` illustrates the localization of cows (from 1 to 16) simultaneously using multiple views. Only applicable to 7/25.

<div align="center">
<video width="800" controls autoplay loop>
  <source src="./files/visual_loc_vid.mp4" type="video/mp4">
</video>
</div>

<a href="./files/visual_loc_vid.mp4">
  <vid src="./files/visual_loc_vid.mp4" width="800">
</a>

