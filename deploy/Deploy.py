import os
import time

import cv2
import numpy as np
from PIL.Image import Image
from ultralytics import YOLO


def load_model():
    model = YOLO('../weights/weight.pt')
    return model

def load_pic_data(path):
    files = os.listdir(path)
    data_path = []
    for file in files:
        if file.find('.png') == -1 and file.find('.jpg') == -1 \
                and file.find('.jpeg') == -1:
            continue
        file = path + '/' + file
        data_path.append(os.path.abspath(file))
    return data_path

def predict(model, picList):
    # seems that input a list has a weaker performance
    # return model(picList)
    results = []
    for pic in picList:
        ResultTemps = model(pic)
        results.append(ResultTemps)
    return results


def plot_result(input_results, result_path, data_path):
    all_dist = os.listdir(data_path)
    pic_dist = []
    for dist in all_dist:
        if dist.find('.png') == -1 and dist.find('.jpg') == -1 \
                and dist.find('.jpeg') == -1:
            continue
        pic_dist.append('Result_' + dist)
    index = 0
    for input_result in input_results:
        res_plotted = input_result[0].plot()
        print(input_result[0])
        time.sleep(100)
        cv2.imwrite(result_path + '/' + pic_dist[index], res_plotted)
        index += 1


if __name__ == '__main__':
    load_model_start_time = time.thread_time()
    Model = load_model()
    print('Load model done:', round(time.thread_time() - load_model_start_time, 3), 's')
    load_data_start_time = time.thread_time()
    Data = load_pic_data('../images')
    print('Load data done:', round(time.thread_time() - load_data_start_time, 3), 's')
    predict_start_time = time.thread_time()
    Results = predict(Model, Data)
    print('Predict done:', round(time.thread_time() - predict_start_time, 3), 's')
    output_result_start_time = time.thread_time()
    plot_result(Results, '../results', '../images')
    print('Output result done:', round(time.thread_time() - output_result_start_time, 3), 's')
    print('Whole process done:', round(time.thread_time() - load_data_start_time, 3), 's')