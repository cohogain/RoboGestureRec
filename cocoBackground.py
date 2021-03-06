import os
import cv2
import numpy as np
from natsort import natsorted

imageFolder ='/home/cohogain/yolo3/clean/'		#images folder
maskFolder ='/home/cohogain/yolo3/mask_clean/'		#segmentations folder
cocoFolder ='/home/cohogain/val2017/'			#coco dataset folder
result_folder ='/home/cohogain/yolo3/clean1/'		#output image folder 

img_entries = natsorted(os.listdir(imageFolder))
mask_entries = natsorted(os.listdir(maskFolder))
coco_entries  = natsorted(os.listdir(cocoFolder))

index = 0
for mask1, img1 in zip(mask_entries, img_entries):
    coco = coco_entries[index]
    index += 1

    img = cv2.imread((os.path.join(imageFolder,img1)))
    mask = cv2.imread((os.path.join(maskFolder,mask1)))
    coco = cv2.imread((os.path.join(cocoFolder, coco)))
    result = img.copy()

    for i in range(0, len(mask)):
        for j in range(0, len(mask[0])):
            if(mask[i,j,0] == 0 and mask[i,j,1] == 0 and mask[i,j,2] == 0):
                result[i,j,0] = coco[i,j,0]
                result[i,j,1] = coco[i,j,1]
                result[i,j,2] = coco[i,j,2]

    cv2.imshow('result',result)
    cv2.waitKey(600)

    ## Merge the mask and crop the red regions
    cv2.imwrite(result_folder +  str(img1), result)


    #Wait until a key is pressed:
    cv2.waitKey(50)

    # Destroy all created windows:
    cv2.destroyAllWindows()
