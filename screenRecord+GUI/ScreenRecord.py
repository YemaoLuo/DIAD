import threading
from datetime import datetime

import numpy as np
from PIL import ImageGrab
from cv2 import CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FRAME_COUNT, CAP_PROP_FPS, VideoCapture, \
    COLOR_RGB2BGR, cvtColor, VideoWriter, VideoWriter_fourcc
from pynput import keyboard


def record_screen():
    global name
    name = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    screen = ImageGrab.grab()
    width, high = screen.size
    fourcc = VideoWriter_fourcc('X', 'V', 'I', 'D')
    video = VideoWriter('%s.mp4' % name, fourcc, 16, (width, high))
    print("record start !!!")
    while True:
        if flag:
            print("record end !!!")
            video.release()
            break
        img = ImageGrab.grab()
        imm = cvtColor(np.array(img), COLOR_RGB2BGR)  # 转为opencv的BGR模式
        video.write(imm)
    # 视频信息
    video = VideoCapture('%s.mp4' % name)
    fps = video.get(CAP_PROP_FPS)
    frames = video.get(CAP_PROP_FRAME_COUNT)
    print('帧率=%.1f' % (fps))
    print('帧数=%.1f' % (frames))
    print('分辨率=(%d,%d)' % (int(video.get(CAP_PROP_FRAME_WIDTH)), int(video.get(CAP_PROP_FRAME_HEIGHT))))
    print('时间=%.2f秒' % (int(frames) / fps))
    return


def on_press(key):  # 监听按键
    global flag
    if key == keyboard.Key.space:
        flag = True
        return False  # 返回False，键盘监听结束


if __name__ == '__main__':
    flag = False
    th = threading.Thread(target=record_screen)
    th.start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    pass
