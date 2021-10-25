
<h1 align="center">Creating the Dataset and Training the Model</h1>

<p align="center">
    This document will provide information on how to create the dataset and run the training on the model. We use <a href="https://github.com/AlexeyAB/darknet">AlexeyAB's version</a> of YOLOv4, so we will look at how we can create the dataset and we will explain in brief how we can train and evaluate our model.
</p>

---

## Table of Contents

1. [Prepare the dataset](#prepare-the-dataset)
1. [Run the training](#run-the-training)
1. [Evaluate the model](#evaluate-the-model)


## Prepare the dataset

- Collect the data packet
- Run split_test_train.py
- Run train.py in the train folder and test.py in the test folder *(have to copy these over from the dev branch)*
- Add the .data file and the .names file

You can find more detailed instructions in the file: **[Annotating-Images-for-ML-Applications.pdf](https://github.com/software3daerospace/treecounter-ML/blob/main/docs/pdf/Annotating-Images-for-ML-Applications.pdf)**

## Run the training:
```sh
 ./darknet.exe detector train data/train/tree-wooden-metal.data cfg/yolov4-custom.cfg yolov4.conv.137
 ```

## Evaluate the model:

```sh
./darknet.exe detector map data/train/tree-wooden-metal.data cfg/yolov4-custom.cfg backup/yolov4-custom_final.weights
```

