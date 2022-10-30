import cv2
from skimage.metrics import structural_similarity
from PIL import ImageGrab
import os
import time
# 获取原图像的水平方向尺寸和垂直方向尺寸
import numpy

posiList = []
heightR, widthR = 200, 300

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


def imagegrab_cv2(interal):
    '''
    间隔抓图转cv2s
    :param interal: 间隔时长
    :return: CV2格式，图片，抓取时间
    '''
    imageA = ImageGrab.grab()
    time.sleep(interal)
    imageB = ImageGrab.grab()
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))

    imageA = numpy.asarray(imageA)
    imageB = numpy.asarray(imageB)

    return imageA, imageB, now


if __name__ == '__main__':
    image = ImageGrab.grab()
    while True:
        # 1920*1080, 1600*900, 1366*768, 1280*720,测s试用'Resources/2021_IOTE_RFID.mp4',"2022-06-07-17_00_49.png"测试用
        # img = cv2.imread("2022-06-15-15_39_20.png")
        img = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)
        ws, hs, w, h = set_region(img)
        if cv2.waitKey(1) & 0xFF == ord("s"):
            break
    print(ws, hs, w, h)