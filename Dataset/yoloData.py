import os
import cv2
import numpy as np
import random
from natsort import natsorted

#filepaths
poseFolder =''								#json pose coords folder
imageFolder =''								#images folder
maskFolder =''								#segmentations folder
result_folder =''							#output folder to check labelling

#sort filenames numerically
img_entries = natsorted(os.listdir(imageFolder))
mask_entries = natsorted(os.listdir(maskFolder))


count = 0
for mask1, img1 in zip(mask_entries, img_entries):

    img = cv2.imread((os.path.join(imageFolder,img1)))
    mask = cv2.imread((os.path.join(maskFolder,mask1)))

    armFront = armOut = armUp = none = False
    leftMost = leftMost1 = leftMost2 = leftMost3 = 432
    rightMost = rightMost1 = rightMost2 = rightMost3 = 0
    upMost = upMost1 = upMost2 = upMost3 = 368
    downMost = downMost1 = downMost2 = downMost3 = 0

    result = img.copy()

    for i in range(0, len(mask)):
        for j in range(0, len(mask[0])):
            if(mask[i,j,0] == 200 and mask[i,j,1] == 200 and mask[i,j,2] == 200):
                armFront = True
                if(j < leftMost):
                    leftMost = j   
                if(i < upMost):
                    upMost = i  

                if(i > downMost):
                    downMost = i  
                if(j > rightMost):
                    rightMost = j

            if(mask[i,j,0] == 210 and mask[i,j,1] == 210 and mask[i,j,2] == 210):
                armOut = True
                if(i > downMost1):
                    downMost1 = i     
                if(i < upMost1):
                    upMost1 = i  
                if(j < leftMost1):
                    leftMost1 = j
                if(j > rightMost1):
                    rightMost1 = j

            if(mask[i,j,0] == 230 and mask[i,j,1] == 230 and mask[i,j,2] == 230):
                armUp = True
                if(j < leftMost2):
                    leftMost2 = j   
                if(i < upMost2):
                    upMost2 = i  

                if(i > downMost2):
                    downMost2 = i  
                if(j > rightMost2):
                    rightMost2 = j

            if(mask[i,j,0] == 240 and mask[i,j,1] == 240 and mask[i,j,2] == 240):
                none = True
                if(i > downMost3):
                    downMost3 = i     
                if(i < upMost3):
                    upMost3 = i  
                if(j < leftMost3):
                    leftMost3 = j
                if(j > rightMost3):
                    rightMost3 = j

    print(str(os.path.join(imageFolder,str(img1))), end =" ")   
    if(armFront == True):
        x, y, w, h = leftMost, upMost, rightMost, downMost
        #cv2.rectangle(result, (x, y), (w, h), (0, 0, 255), 2)
        print(str(x) + ','+ str(y) + ','+ str(w) + ','+ str(h) +',' + str(0), end=" ")
    if(armOut == True):
        x1, y1, w1, h1 = leftMost1, upMost1, rightMost1, downMost1
        #cv2.rectangle(result, (x1, y1), (w1, h1), (0, 0, 255), 2)
        print(str(x1) + ','+ str(y1) + ','+ str(w1) + ','+ str(h1) +',' + str(1), end=" ")
    if(armUp == True):
        x2, y2, w2, h2 = leftMost2, upMost2, rightMost2, downMost2
        #cv2.rectangle(result, (x2, y2), (w2, h2), (0, 0, 255), 2)
        print(str(x2) + ','+ str(y2) + ','+ str(w2) + ','+ str(h2) +',' + str(2), end=" ")
    if(none == True):
        x3, y3, w3, h3 = leftMost3, upMost3, rightMost3, downMost3
        #cv2.rectangle(result, (x3, y3), (w3, h3), (0, 0, 255), 2)
        print(str(x3) + ','+ str(y3) + ','+ str(w3) + ','+ str(h3) +',' + str(3), end=" ")
    print("")
	
    ## Merge the mask and crop the red regions
    cv2.imwrite(result_folder +  str(img1), result)

    #cv2.imshow("act_img", result)
    count = count + 1

    cv2.waitKey(1)
