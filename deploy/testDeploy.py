import os
import time

from ultralytics import YOLO


def load_model():
    model = YOLO('../weights/weight.pt')
    return model


def predict(model, picList):
    results = []
    for pic in picList:
        results.append(model(pic))
    return results


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


if __name__ == '__main__':
    load_model_start_time = time.thread_time()
    Model = load_model()
    print('Load model done:', round(time.thread_time() - load_model_start_time, 3), 's')
    load_data_start_time = time.thread_time()
    Data = load_pic_data('../images')
    print('Load data done:', round(time.thread_time() - load_data_start_time, 3), 's')
    predict_start_time = time.thread_time()
    Results = predict(Model, Data)
    for result in Results:
        print(result)
    print('Predict done:', round(time.thread_time() - predict_start_time, 3), 's')
