import cv2
import numpy as np
from ultralytics import YOLO


def load_model():
    model = YOLO('../weights/weight.pt')
    return model


# def predict(model, mss_image):
#     cv2_image = cv2.cvtColor(np.array(mss_image), cv2.COLOR_RGBA2RGB)
#     result_temp = model(cv2_image)
#     detected_image = result_temp[0].plot(show_conf=False)
#     return detected_image
def predict(model, mss_image):
    cv2_image = cv2.cvtColor(np.array(mss_image), cv2.COLOR_RGBA2RGB)
    result_temp = model(cv2_image)

    detected_objects = []
    detections = result_temp[0].boxes

    for detection in detections:
        # 获取类别索引
        cls_index = int(detection.cls.squeeze())
        # 从类名列表中获取类名
        class_name = model.names[cls_index]
        # print(f"Detected class: {class_name}")
        detected_objects.append(class_name)
        # print(detected_objects)
    print(detected_objects)

    detected_image = result_temp[0].plot(show_conf=False)
    return detected_image, detected_objects


def plot_result(input_results, result_path):
    index = 0
    color = (0, 0, 255)
    for input_result in input_results:
        res_plotted = input_result[0].plot(show_conf=False)
        cv2.imwrite(result_path + '/Result_' + str(index) + '.png', res_plotted)
        index += 1
