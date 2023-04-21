import os
import time

import cv2
import numpy as np
from PIL.Image import Image
from ultralytics import YOLO


def load_model():
    model = YOLO('../weights/weight.pt')
    return model

def detect(input_image):
    Result1 = Model(input_image)#用之前需要load model，为了效率已经把loadmodel写在在打开软件的时候
    # print("Result1",Result1)
    res_plotted = Result1[0].plot(show_conf=False)
    # print("res_plotted",res_plotted)
    # cv2.imshow('result', res_plotted)
    # cv2.waitKey(1) 把注释去掉就能显示图像
    return res_plotted

if __name__ == '__main__':
    Model = load_model()
    # 调用示例
    # img = detect('C:/Users/25779/Desktop/DIAD/DIAD/DIAD/copylym/DIAD/images/05_20_27_625.png')