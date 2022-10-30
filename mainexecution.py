import cv2
from skimage.metrics import structural_similarity
from PIL import ImageGrab
import numpy
import time
import os

posiList = []

def mouse_click(events, x, y, flags, params):
    '''

    :param events:
    :param x:
    :param y:
    :param flags:
    :param params:
    :return:
    '''
    global x1, y1, x2, y2
    if events == cv2.EVENT_LBUTTONDOWN:
        posiList.append((x, y))

    elif events == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):
        posiList.append((x, y))

    elif events == cv2.EVENT_RBUTTONDOWN:
        posiList.clear()

def set_region(img):
    height, width = img.shape[:2]
    # img.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    # img.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    posiwstart = 0
    posihstart = 0
    posiw = width
    posih = height

    if len(posiList) > 1:
        posiwstart = posiList[0][0]
        posihstart = posiList[0][1]
        posiw = posiList[-1][0]
        posih = posiList[-1][1]
        if posiw > width:
            posiw = width
        elif posih > height:
            posih = height
        cv2.rectangle(img, posiList[0], (posiw, posih), (255, 0, 255), 2)
        widthc = abs(posiwstart-posiw)
        heightc = abs(posihstart-posih)
        cv2.putText(img, 'W:'+str(widthc)+' H:'+str(heightc)+" Tips:'S' Click to Choose& Right Mouse Click to remove rectangle",
                    (posiList[0][0], posiList[0][1]-8), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
# openCV全屏显示，下面两句话需要一起使用
    cv2.namedWindow("Original", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Original", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Original", img)
    cv2.setMouseCallback("Original", mouse_click)
    # cv2.waitKey(1)
    return posiwstart, posihstart, posiw, posih

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
    image = ImageGrab.grab()
    while True:
        img = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)
        ws, hs, w, h = set_region(img)
        if cv2.waitKey(1) & 0xFF == ord("s"):
            break
    print(ws, hs, w, h)
# 如何能离开当前的截屏？
    bbox2 = (ws, hs, w, h)
    cv2.destroyAllWindows()
    print(bbox2)
    while True:
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