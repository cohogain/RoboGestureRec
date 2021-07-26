# RoboGestureRec

**Description:**

This project compares the use of pose estimation and object detection to perform gesture recognition in a RoboCup environment.                                    
Both 'Openpose', human pose estimation algorithm and 'YoloV3', object detection algorithm are implemented using Tensorflow.

**Original Repos:**

The repos used in this project are found below. Please follow the download instructions provided by these repos.

Pose estimation repo : https://github.com/jiajunhua/ildoonet-tf-pose-estimation                                                                                   
Object Detection repo : https://github.com/wizyoung/YOLOv3_TensorFlow


![alt text](https://github.com/cohogain/RoboGestureRec/blob/main/object_detection.png) ![alt text](https://github.com/cohogain/RoboGestureRec/blob/main/pose_estimation.png)





**Datasets:**

The datasets used for training were generated using UERoboCup (RoboCup scene generator : https://github.com/TimmHess/UERoboCup).
The data exported by this program consists of coloured images, segmantic segmentations and robot joint image coordinates.

Use **openposeData.py** to structure the data into the necessary format for openpose training.                                                          
Similarly, use **yoloData.py** to structure the data into the required yolov3 format for training.

The background of the images are converted to images taken from COCO 2014 validation set to create a more dynamic environment to achieve better machine learning. Use **cocoBackground.py** to complete this background conversion.

The raw data, correctly formatted datasets and COCO val 2014 can be found at the following link.

The data used can be found at the following Google Drive link: 
https://drive.google.com/drive/folders/1GEHBlKblf6MOj6l6uPikD92NkXQP0iLF?usp=sharing




