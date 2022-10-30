from PIL import ImageGrab
import time
from skimage.metrics import structural_similarity
import cv2
import numpy
import os


def pic_record(frame, folder_name):
    '''
    按帧截取视频中的所有图片，图片会存到视频当前目录下的同名文件夹中
    :param file: 文件地址，文件名.文件格式
    :return: None
    '''
    if os.path.exists(folder_name):
        pass
    else:
        os.makedirs(folder_name)

    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    frame.save(r"{0}\{0}{1}.png".format(folder_name, now))
    print(r"{0}\{0}{1}.png".format(folder_name, now))


if __name__ == '__main__':
    ws, hs, w, h = 585, 160, 1898, 892
    bbox2 = (219, 246, 1699, 1079)
    # bbox2 = (106, 42, 1816, 1002)
    # bbox2 = (520, 285, 1614, 903)
    # ws, hs, w, h = 0, 0, 1920, 1080
    while True:
        # ImageGrab.grab(bbox =(0, 0, 300, 300))
        imageA = ImageGrab.grab()
        time.sleep(2)
        imageB = ImageGrab.grab()
        image1 = imageA.crop(bbox2)
        image2 = imageB.crop(bbox2)

        # convert the images to grayscale
        grayA = cv2.cvtColor(numpy.asarray(image1), cv2.COLOR_RGB2GRAY)
        grayB = cv2.cvtColor(numpy.asarray(image2), cv2.COLOR_RGB2GRAY)

        # compute the structural Similarity Index(SSIM) between the two images, ensuring that the difference image is returned
        (score, diff) = structural_similarity(grayA, grayB, full=True)
        print("SSIM:{}".format(score))
        if score < 0.9:
            pic_record(imageB, 'wuyuan')
            pic_record(image2, 'wuyuanppt')