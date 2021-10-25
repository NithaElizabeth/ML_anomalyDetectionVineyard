## Testing and Utility Scripts:

In this directory, you will find various small scripts which do not contribute directly to the final application, but aid in the various steps before, after, and during the testing of the application.
The functionalities of the scripts are explained in the later sections. The scripts are divided into two broad sections - **test** scripts, which had been used to test out certain functionalities, and **util** scripts, which aim to automate otherwise daunting manual tasks.

Click on the drop-down link next to a script to view its functionality:

<details close>
<summary> convert-to-excel.py </summary>
<br>
The script `convert-to-excel.py` generates a spreadsheet in the XLSX format, which contains important information about our dataset. This includes the image properties *(path, type, filename)*, the parcel number, the vineyard information, the weather information, and so on.

#### Usage instructions:

- Copy this file on to the root directory of the dataset
- Run the script `python3 convert-to-excel.py`
- This will read from the pre-generated `train.txt` file, and fill in the missing information in the spreadsheet.

**Note:** This file requires the *train.txt* or *test.txt* to be generated in advance.
</details>

<details close>
<summary> create-dataset.py </summary>
<br>
This scripts extracts images from all the videos in a given directory to generate a dataset of images in the output directory specified.

#### Usage instructions:

```python
python3 scripts/create-dataset.py \
-iv <path-to-input-videos> \
-ov <path-to-output-videos>
```
</details>

<details close>
<summary> create-video.py </summary>
<br>
This file creates an AVI video from a directory of images. Useful when running inference/validation on static frames and exporting the images as a video.

#### Usage instructions:

- Copy the script to the directory where the images are stored.
- Run the script `python3 scripts/create-video.py`
- This will let the script read each image in the directory and pack them into a video.

</details>

<details close>
<summary> detect-trees.py </summary>
<br>
The script `detect-trees.py` takes in an input video and detects the trees in the video. This the staging script to the main script in the root directory.

#### Usage instructions:

You can run the script from the root directory as follows:

```python
python3 scripts/detect-trees.py \
-iv videos/video3.mp4  \
-ov videos/test.avi \
-cfg models/yolov3/cfg/yolov3_custom.cfg \
-w models/yolov3/weights/yolov3_custom_final.weights \
-c models/yolov3/classes.names
```

This will generate the `test.avi` file in the videos/ directory
</details>

<details close>
<summary> detect-darknet.py </summary>
<br>
The script `detect-darknet.py` takes in an input image and detects the objects of interest *(trees, metal posts, wooden posts)* in the image.

#### Usage instructions:

You can run the script from the root directory as follows:

```python
python3 scripts/detect-darknet.py \
-iv imgs/img-1.jpg  \
-cfg models/yolov3/cfg/yolov3_custom.cfg \
-w models/yolov3/weights/yolov3_custom_final.weights \
-c models/yolov3/classes.names
```

This will generate the `predictions.jpg` file in the videos/ directory
</details>
