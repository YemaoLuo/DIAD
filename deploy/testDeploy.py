import os
import time

from ultralytics import YOLO


def load_model():
    model = YOLO('../weights/weight.pt')
    return model


def getClass(Class):
    label_file = open('../labels/labels.txt')
    lines = label_file.readlines()
    label_file.close()
    return lines[Class].replace('\n', '')


def predict(model, picList):
    # seems that input a list has a weaker performance
    # return model(picList)
    results = []
    for pic in picList:
        ResultTemps = model(pic)
        index = 0
        for ResultTemp in ResultTemps:
            ResultTemps[index] = ResultTemp.boxes
            index += 1
        results.append(ResultTemps)
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
    # note that might have multiple results in one graph should be all handled properly
    # for Result in Results:
    #     print('=' * 50)
    #     print('Class:', getClass(Result.cls.int()))
    #     print('Confidence:', round(float(Result.conf) * 100, 2), '%')
    #     print('Position:', Result.xywhn, Result.xyxyn)
    #     print('Predict done:', round(time.thread_time() - predict_start_time, 3), 's')
