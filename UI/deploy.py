import cv2
import mss
from ultralytics import YOLO
import numpy as np

def load_model():
    model = YOLO('../weights/weight.pt')
    return model

def predict(model, mss_image):
    cv2_image = cv2.cvtColor(np.array(mss_image), cv2.COLOR_RGBA2RGB)
    result_temp = model(cv2_image)
    detected_image = result_temp[0].plot(show_conf=False)
    return detected_image


def plot_result(input_results, result_path):
    index = 0
    for input_result in input_results:
        res_plotted = input_result[0].plot(show_conf=False)
        cv2.imwrite(result_path + '/Result_' + str(index) + '.png', res_plotted)
        index += 1


# 测
if __name__ == '__main__':
    Model = load_model()
    print('Load model done')

    # 截图
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 1000, "height": 800}
        mss_image = sct.grab(monitor)

    Results = predict(Model, mss_image)
    print('Predict done')

    plot_result(Results, '../results')
    print('Output result done')