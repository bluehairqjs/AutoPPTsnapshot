import cv2
from cv2 import VideoCapture
import numpy as np
import os
import time
from skimage.metrics import structural_similarity

def save_image(image, addr, num):
    address=addr +str(num)+'.png'
    cv2.imwrite(address,image)

if __name__ == '__main__':
    video_path = 'C:/Users/Jisong Qu/'
    file_name ='20221026_161926.mp4'
    f_save_path ='D:/imageoutput/1/'
    videoCapture = cv2.VideoCapture(video_path+file_name)
    success, frame = videoCapture.read()
    print(success)
    count=0
    score = 0
    timeFrame= int(videoCapture.get(cv2.CAP_PROP_FPS))
    while success:
        if (count % timeFrame==0):
            if score <0.9:
                save_image(frame,f_save_path+file_name.split('.')[0],count)
                grayA = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2GRAY)
                print('save image:',count, 'score:',score)
        success, frame = videoCapture.read()
        grayB = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2GRAY)
        (score, diff) = structural_similarity(grayA, grayB, full=True)
        print('count:',count,'score:',score)
        count +=1
        