import json
import os
import numpy as np
import cv2
from natsort import natsorted

def print_categories():
    print('{', end ="")
    print('"id": ' + str(1)+ ',', end =" ")
    print('"name": "Nao" ,', end =" ")
    print('"keypoint_colors": ["#d0d957", "#0b5e73", "#0000ff", "#730b5e", "#ff8533", "#518c0e", "#82c7d9", "#0000d9", "#ff1ab3", "#733c17", "#7cff4d", "#1ab3ff", "#0000cc"]' + ',', end =" ")
    print('"skeleton": [[1, 2], [1, 3], [2, 4], [3, 5], [6, 8], [7, 9], [8, 10], [9, 11], [12, 14], [13, 15], [14, 16], [15, 17]]', end =" ")
    print('}', end ="")

def print_keypoints(keypoints):
    x_min = 432 
    y_min = 368 
    x_max = 0
    y_max = 0 
    x_count = 0
    numKeypoints = 0;
    count=0

    print('{', end ="")
    print('"id": ' + str(keypoint_id)+ ',', end =" ")
    print('"image_id": ' + str(image_id) + ',', end =" ")
    print('"category_id": ' + str(1)+ ',', end =" ")

    #find min and max x,y coordinates for bounding box
    for k in range(0, len(keypoints),3):
        if(keypoints[x_count] < x_min and keypoints[x_count] > 0):
            x_min = keypoints[x_count]
        if(keypoints[x_count] > x_max):
            x_max = keypoints[x_count]
        if(keypoints[x_count+1] < y_min and keypoints[x_count+1] > 0):
            y_min = keypoints[x_count+1]
        if(keypoints[x_count+1] > y_max):
            x_count+=3

    #count number of keypoints
    for j in range(0, len(keypoints)-1, 3):
        if(keypoints[count] != 0 and keypoints[count+1] != 0 and keypoints[count+2] != 0):
            numKeypoints+=1
        count+=3

    #print bounding box and area
    if(numKeypoints == 0):
        print('"bbox": [0,0,0,0]', end =", ")
        print('"area": 0', end =", ")
    else:
        print('"bbox": [' + str(int(x_min)) + ',' + str(int(y_min)) + ',' + str(int(x_max-x_min)) + ',' + str(int(y_max-y_min)) + ']', end =", ")
        print('"area": ' + str(int((x_max-x_min) * (y_max-y_min))), end =", ")
    print('"iscrowd": false ', end =", ")

    #print keypoints coords
    print('"keypoints": [', end =" ")
    for i in range(0, len(keypoints)):
        if(i != len(keypoints)-1):
            print(str(int(keypoints[i])) + ', ', end =" ")
        else:
            print(str(int(keypoints[i])) + '], ', end =" ")
    print('"num_keypoints": ' + str(numKeypoints), end ="} ")

def print_images(entry):
    print('{', end ="")
    print('"id": ' + str(image_id) + ',', end =" ")
    print('"path": "' + str(os.path.join(imageFolder,entry))+ '",', end =" ")
    print('"width": ' + str(len(image_1[0]))+ ',', end =" ")
    print('"height": ' + str(len(image_1))+ ',', end =" ")
    print('"file_name": "' + str(entry) + '"' ,end =" ")

#keypoint array to hold 17 (x,y,v) values
keypoints = np.zeros(shape=(51,1))
keypoint_id = 0
image_id = 0


poseFolder ='/media/cohogain/UUI/bigYOLO/Pose1/35'
imageFolder ='/media/cohogain/UUI/bigYOLO/35'
result_folder ='/media/cohogain/UUI/bigYOLO/checkTestPose/'

#read in images and pose coordinates
img_entries = natsorted(os.listdir(imageFolder))
pose_entries = natsorted(os.listdir(poseFolder))

#print image info
print('{"images": [', end ="")
for entry in img_entries:
    image_1 = cv2.imread((os.path.join(imageFolder,entry)))
    print_images(entry)
    if(entry != img_entries[-1]):
        print('}' + ',', end =" ")
    else:
        print('}', end ="")
    image_id += 1
print('],', end =" ")

#print category info
print('"categories": [', end ="")
print_categories()
print('],', end =" ")

#print annotation info
image_id = 0
count = 0
print('"annotations": [', end ="")
for pose,img in zip(pose_entries,img_entries):
    image_1 = cv2.imread((os.path.join(imageFolder,img)))
    file_path = os.path.join(poseFolder,pose)
    leftMost = 432
    rightMost = 0
    upMost = 368
    downMost = 0
    leftMost1 = 432
    rightMost1 = 0
    upMost1 = 368
    downMost1= 0
    with open(file_path) as f:
        data = json.loads(f.read())
        for i in range(0, len(data)):
            if(i != len(data)):
                for j in range(0,len(keypoints)):
                    keypoints[j] = 0
                if('L_Shoulder' in data[i]):
                    #Lsho
                    keypoints[15] = int(data[i]['L_Shoulder'].split(',')[0])
                    keypoints[16] = int(data[i]['L_Shoulder'].split(',')[1])
                    keypoints[17] = 2
                    if(keypoints[15] >= 432 or keypoints[15] < 0 or keypoints[16] >= 368 or keypoints[16] < 0):
                        keypoints[15] = 0
                        keypoints[16] = 0
                        keypoints[17] = 0
                    #cv2.circle(image_1, (keypoints[15], keypoints[16]), 3, (0, 0, 255), -1)
                if('R_Shoulder' in data[i]):
                    #Rsho
                    keypoints[18] = int(data[i]['R_Shoulder'].split(',')[0])
                    keypoints[19] = int(data[i]['R_Shoulder'].split(',')[1])
                    keypoints[20] = 2
                    if(keypoints[18] >= 432 or keypoints[18] < 0 or keypoints[19] >= 368 or keypoints[19] < 0):
                        keypoints[18] = 0
                        keypoints[19] = 0
                        keypoints[20] = 0
                    #cv2.circle(image_1, (keypoints[18], keypoints[19]), 3, (0, 0, 255), -1)
                if('L_Elbow' in data[i]):
		            #Lelb
                    keypoints[21] = int(data[i]['L_Elbow'].split(',')[0])
                    keypoints[22] = int(data[i]['L_Elbow'].split(',')[1])
                    keypoints[23] = 2
                    if(keypoints[21] >= 432 or keypoints[21] < 0 or keypoints[22] >= 368 or keypoints[22] < 0):
                        keypoints[21] = 0
                        keypoints[22] = 0
                        keypoints[23] = 0
                    #cv2.circle(image_1, (keypoints[21], keypoints[22]), 3, (0, 0, 255), -1)
                if('R_Elbow' in data[i]):
		            #Relb
                    keypoints[24] = int(data[i]['R_Elbow'].split(',')[0])
                    keypoints[25] = int(data[i]['R_Elbow'].split(',')[1])
                    keypoints[26] = 2
                    if(keypoints[24] >= 432 or keypoints[24] < 0 or keypoints[25] >= 368 or keypoints[25] < 0):
                        keypoints[24] = 0
                        keypoints[25] = 0
                        keypoints[26] = 0
                    #cv2.circle(image_1, (keypoints[24], keypoints[25]), 3, (0, 0, 255), -1)
                if('L_Wrist' in data[i]):
		            #Lwri
                    keypoints[27] = int(data[i]['L_Wrist'].split(',')[0])
                    keypoints[28] = int(data[i]['L_Wrist'].split(',')[1])
                    keypoints[29] = 2
                    if(keypoints[27] >= 432 or keypoints[27] < 0 or keypoints[28] >= 368 or keypoints[28] < 0):
                        keypoints[27] = 0
                        keypoints[28] = 0
                        keypoints[29] = 0
                    #cv2.circle(image_1, (keypoints[27], keypoints[28]), 3, (0, 0, 255), -1)
                if('R_Wrist' in data[i]):
		            #Rwri
                    keypoints[30] = int(data[i]['R_Wrist'].split(',')[0])
                    keypoints[31] = int(data[i]['R_Wrist'].split(',')[1])
                    keypoints[32] = 2
                    if(keypoints[30] >= 432 or keypoints[30] < 0 or keypoints[31] >= 368 or keypoints[31] < 0):
                        keypoints[30] = 0
                        keypoints[31] = 0
                        keypoints[32] = 0
                    #cv2.circle(image_1, (keypoints[30], keypoints[31]), 3, (0, 0, 255), -1)
                if('L_Hip' in data[i]):
		            #Lhip
                    keypoints[33] = int(data[i]['L_Hip'].split(',')[0])
                    keypoints[34] = int(data[i]['L_Hip'].split(',')[1])
                    keypoints[35] = 2
                    if(keypoints[33] >= 432 or keypoints[33] < 0 or keypoints[34] >= 368 or keypoints[34] < 0):
                        keypoints[33] = 0
                        keypoints[34] = 0
                        keypoints[35] = 0
                    #cv2.circle(image_1, (keypoints[33], keypoints[34]), 3, (0, 0, 255), -1)
                if('R_Hip' in data[i]):
		            #Rhip
                    keypoints[36] = int(data[i]['R_Hip'].split(',')[0])
                    keypoints[37] = int(data[i]['R_Hip'].split(',')[1])
                    keypoints[38] = 2
                    if(keypoints[36] >= 432 or keypoints[36] < 0 or keypoints[37] >= 368 or keypoints[37] < 0):
                        keypoints[36] = 0
                        keypoints[37] = 0
                        keypoints[38] = 0
                    #cv2.circle(image_1, (keypoints[36], keypoints[37]), 3, (0, 0, 255), -1)
                if('L_Knee' in data[i]):
		            #Lknee
                    keypoints[39] = int(data[i]['L_Knee'].split(',')[0])
                    keypoints[40] = int(data[i]['L_Knee'].split(',')[1])
                    keypoints[41] = 2
                    if(keypoints[39] >= 432 or keypoints[39] < 0 or keypoints[40] >= 368 or keypoints[40] < 0):
                        keypoints[39] = 0
                        keypoints[40] = 0
                        keypoints[41] = 0
                    #cv2.circle(image_1, (keypoints[39], keypoints[40]), 3, (0, 0, 255), -1)
                if('R_Knee' in data[i]):
		            #Rknee
                    keypoints[42] = int(data[i]['R_Knee'].split(',')[0])
                    keypoints[43] = int(data[i]['R_Knee'].split(',')[1])
                    keypoints[44] = 2
                    if(keypoints[42] >= 432 or keypoints[42] < 0 or keypoints[43] >= 368 or keypoints[43] < 0):
                        keypoints[42] = 0
                        keypoints[43] = 0
                        keypoints[44] = 0
                    #cv2.circle(image_1, (keypoints[42], keypoints[43]), 3, (0, 0, 255), -1)
                if('L_Ankle' in data[i]):
		            #Lank
                    keypoints[45] = int(data[i]['L_Ankle'].split(',')[0])
                    keypoints[46] = int(data[i]['L_Ankle'].split(',')[1])
                    keypoints[47] = 2
                    if(keypoints[45] >= 432 or keypoints[45] < 0 or keypoints[46] >= 368 or keypoints[46] < 0):
                        keypoints[45] = 0
                        keypoints[46] = 0
                        keypoints[47] = 0
                    #cv2.circle(image_1, (keypoints[45], keypoints[46]), 3, (0, 0, 255), -1)
                if('R_Ankle' in data[i]):
		            #Rank
                    keypoints[48] = int(data[i]['R_Ankle'].split(',')[0])
                    keypoints[49] = int(data[i]['R_Ankle'].split(',')[1])
                    keypoints[50] = 2
                    if(keypoints[48] >= 432 or keypoints[48] < 0 or keypoints[49] >= 368 or keypoints[49] < 0):
                        keypoints[48] = 0
                        keypoints[49] = 0
                        keypoints[50] = 0
                    #cv2.circle(image_1, (keypoints[48], keypoints[49]), 3, (0, 0, 255), -1)

            print_keypoints(keypoints)
            keypoint_id += 1

            if(pose != pose_entries[-1]):
                print(',', end =" ")
            if(pose == pose_entries[-1] and i < len(data)-1):
                print(',', end =" ")

        image_id += 1
        cv2.imwrite(result_folder +  str(pose) + '.jpg' , image_1)
        count += 1

       # Wait until a key is pressed:
        cv2.waitKey(50)

        # Destroy all created windows:
        cv2.destroyAllWindows()
print(']}', end =" ")












