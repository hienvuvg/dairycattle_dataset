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
* ```uwb_localization.py``` illustrates the localization of a single cow using UWB.
* ```visual_localization.py``` illustrates the localization of cows (from 1 to 16) simultaneously using multiple views. Only applicable to 7/25.


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

**gif files visualizing the program**