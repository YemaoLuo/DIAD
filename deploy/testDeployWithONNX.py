import os
import time

import cv2
import numpy as np
import onnxruntime as ort
import torch
import torch.nn.functional as F
from torchvision import models

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def load_labels(path):
    label = []
    file = open(path)
    labels = file.readlines()
    file.close()
    for item in labels:
        label.append(item.replace('\n', ''))
    return label


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


def predict_imgs(img_paths):
    labels = load_labels('../labels/labels.txt')
    for img_path in img_paths:
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
        img = cv2.resize(img, (640, 640))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 把图片BGR变成RGB
        # print(img.shape)

        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, 0)
        img = img.astype(np.float32)
        img /= 255
        # print(img.shape)

        outputs = ort_session.run(
            None,
            {"images": img.astype(np.float32)},
        )
        # print(np.max(outputs[0]))
        # print(np.argmax(outputs[0]))

        out = torch.tensor(outputs[0], dtype=torch.float64)
        out = F.softmax(out, dim=1)
        proba, class_id = torch.max(out, 1)
        proba = float(proba[0][0])
        id = int(class_id[0][0])
        # print(labels)
        # print('Class :', labels[id])
        # return
        img = img.squeeze(0)
        new_img = np.transpose(img, (1, 2, 0))
        # plt.imshow(new_img)
        # plt.title("predicted class: %s .  probability: %3f" % (labels[id], proba))
        print('predicted class:', labels[id], 'probability:', round(proba * 100, 2), '%')
        # plt.show()


if __name__ == '__main__':
    load_model_start_time = time.thread_time()
    classes = models.AlexNet_Weights.IMAGENET1K_V1.value.meta["categories"]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    picList = load_pic_data('../images')
    model_path = '../weights/weight.onnx'
    load_data_start_time = time.thread_time()
    ort_session = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider'])
    # ndarray =torch.tensor.numpy()
    predict_start_time = time.thread_time()
    predict_imgs(picList)
    print('Predict done:', round(time.thread_time() - predict_start_time, 3), 's')
