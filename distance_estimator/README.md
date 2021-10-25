# Distance estimation for missing/dead tree detection
This folder contains the code for calculating the distance between trees based on the captured images from e-Hermes receiver.



## Currently Supported Custom Functions and Flags
*  Counting the number of total detections (*issue of dupliction not considered*)
*  Counting the number of detection per class i.e. trees, metal post and wooden post (*issue of dupliction not considered*)
*  Left and right rank detections
*  Distance estimation (*in between trees*)
*  Missing tree detection
*  Projecting the trees to a 2D plot - rank by rank
*  Projection of entire vineyard in a single plot





## Running the system

```bash
# TensorFlow CPU
pip install -r requirements.txt

# TensorFlow GPU
pip install -r requirements-gpu.txt
```

## Download the Trained Weights
Download the weights from https://github.com/software3daerospace/treecounter-ML  and paste it inside checkpoints folder



#### Distance estimation
To calculate the distance between the trees image by image :
```
# Run yolov4 model while counting total objects detected
python count.py --weights ./checkpoints/custom-416 --model yolov4 --images [path to test image] --count
```
Running the above command will count the total number of trees detected and calculates the distance:
![detection1](https://user-images.githubusercontent.com/79135954/112763816-1ec7f300-9017-11eb-9252-ce247f854add.png)

NOTE: *THE ABOVE METHOD IS NO LONGER IN USE*

To find the missing trees and to output its details in a structured file :
```
# Run yolov4 model for identifying the missing trees and to generate the json file from the tracked tree details
python missdead_tree_detector.py
```
Make sure to manually change the name of the input JSON files in the script at line number 276 in-order to run the code for different JSON files. \


To project the trees on image to a 2d plot :
```
python projection.py
```
Running the above command will project the trees tracked on a frame to a 2D plot:
![new_left](https://user-images.githubusercontent.com/79135954/114925976-d6933800-9e40-11eb-8cb8-3a1fcb43f3e0.PNG)

To get the projection of the entire vineyard in a single plot :
```
python project_vineyard.py
```
Running the above command will produce the projection of the entire vineyard in a 2D plot:
![image](https://user-images.githubusercontent.com/79135954/117030580-d637df80-ad10-11eb-9a93-8e698c361bca.png)
