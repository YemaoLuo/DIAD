# -*- coding: utf-8 -*-
from PIL import ImageGrab
from pynput import keyboard
import numpy as np
import cv2
import threading
import time
import os
from tkinter import *
from tkinter.ttk import Combobox
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import pyautogui as pag

class App:
    def __init__(self):
        self.StartSelectEnd =0
        self.EndSelectEnd=0
        self.MainWindow = Tk()
        self.MainWindow.title('录屏')
        self.MainWindow.resizable(0, 0)
        # self.MainWindow.overrideredirect(True)
        self.MainWindow.iconbitmap('icon.ico')

        self.res_frame = Frame(self.MainWindow)
        self.res_frame.configure(height=200, width=5000)
        #调节视频分辨率
        self.lb_resolution = Label(self.res_frame, text='视频分辨率')
        self.lb_resolution.pack(side=LEFT, padx=5)
        cb_res_var = StringVar()
        self.cb_resolution = Combobox(self.res_frame, textvariable=cb_res_var, state='readonly', width=4)
        self.cb_resolution['value'] = ('全屏', '0.9x', '0.8x', '0.7x', '0.6x', '0.5x', '0.4x', '0.3x', '0.2x', '0.1x')
        self.cb_resolution.current(5)
        self.cb_resolution.pack(side=LEFT, padx=5)
        # 调节视频倍速
        self.lb_speed = Label(self.res_frame, text='视频倍速')
        self.lb_speed.pack(side=LEFT, padx=5)
        cb_speed_var = StringVar()
        self.cb_speed = Combobox(self.res_frame, textvariable=cb_speed_var, state='readonly', width=4)
        self.cb_speed['value'] = (
        '0.1x', '0.2x', '0.4x', '0.6x', '0.8x', '1.0x', '2.0x', '4.0x', '6.0x', '8.0x', '10.0x')
        self.cb_speed.current(5)
        self.cb_speed.pack(side=LEFT, padx=5)
        #调节帧率
        self.lb_fps = Label(self.res_frame, text='帧率')
        self.lb_fps.pack(side=LEFT, padx=5)
        cb_fps_var = StringVar()
        self.cb_fps = Combobox(self.res_frame, textvariable=cb_fps_var, state='readonly', width=4)
        self.cb_fps['value'] = (
            '5', '10', '15', '20', '25', '30')
        self.cb_fps.current(0)
        self.cb_fps.pack(side=LEFT, padx=5)
        self.var_hide = BooleanVar()
        self.var_hide.set(False)
        self.cbtn_hide = Checkbutton(self.res_frame, text='录屏开始隐藏主窗口', variable=self.var_hide)
        self.cbtn_hide.pack(side=RIGHT, padx=5)
        self.res_frame.grid(row=0, column=0, padx=5, pady=5, sticky=E + S + W + N)

        self.save_frame = Frame(self.MainWindow)
        self.btn_save = Button(self.save_frame, text='选择视频保存地址', width=15, height=1, command=self.saveFile, relief=SOLID,
                               bd=1)
        self.btn_save.pack(side=RIGHT, padx=10)
        self.save_frame.grid(row=1, column=0, padx=5, pady=5, sticky=E + S + W + N)
        self.filename = StringVar()
        # self.filename.set('outvideo.mp4')
        self.lb_save = Label(self.save_frame, textvariable=self.filename, height=1, borderwidth=2, anchor='w',
                             relief=FLAT, bg='lightblue')
        self.lb_save.pack(side=LEFT, padx=5, expand=True, fill=BOTH)
        #开始录制按钮
        self.btn_frame = Frame(self.MainWindow)
        self.btn_start = Button(self.btn_frame, text="开始录制", command=self.start_record, height=1, width=12,
                                relief=SOLID, bd=1)
        self.btn_start.pack(side=LEFT, padx=5)
        #选择起始点
        # cv2.namedWindow('image')
        # # self.btn_frame = Frame(self.MainWindow)
        self.btn_Select = Button(self.btn_frame, text="选择屏幕录制区域", command=self.SelectStartPoint, height=1, width=12,
                                relief=SOLID, bd=1)
        self.btn_Select.pack(side=LEFT, padx=5)
        #结束录制按钮
        self.btn_stop = Button(self.btn_frame, text="结束录制", command=self.stop_record, state=DISABLED, height=1,
                               width=12, relief=SOLID, bd=1)
        self.btn_stop.pack(side=LEFT, padx=5)
        self.btn_exit = Button(self.btn_frame, text='退出', command=self.on_closing, height=1, width=8, relief=SOLID,
                               bd=1)
        self.btn_exit.pack(side=RIGHT, padx=5)
        self.running = StringVar()
        self.running.set('等待开始')
        self.lb_running = Label(self.btn_frame, textvariable=self.running, height=1, borderwidth=1, anchor='w',
                                relief=FLAT, bg='orange')
        self.lb_running.pack(side=LEFT, padx=5, expand=True, fill=BOTH)

        self.btn_frame.grid(row=2, column=0, padx=5, pady=5, sticky=E + S + W + N)

        self.info_frame = Frame(self.MainWindow)
        self.lb_hotkey = Label(self.info_frame, text='快捷键说明：Ctrl+k 开始，Ctrl+y 结束。')
        self.lb_hotkey.pack(side=LEFT, padx=5)
        self.lb_info = Label(self.info_frame, text='DIAD', fg='blue')
        self.lb_info.pack(side=RIGHT, padx=5)
        self.info_frame.grid(row=3, column=0, padx=5, pady=5, sticky=E + S + W + N)
        #设置窗口位置
        self.MainWindow.update()  # 刷新窗口以保证能够获得窗口尺寸
        screenWidth = self.MainWindow.winfo_screenwidth()  # 获得屏幕宽
        screenHeight = self.MainWindow.winfo_screenheight()  # 获得屏幕高
        w = self.MainWindow.winfo_width()  # 获得窗口宽
        h = self.MainWindow.winfo_height()  # 获得窗口高
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.MainWindow.geometry('%dx%d+%d+%d' % (w, h, x, y))  # 窗口屏幕居中显示
        # ------------------------------------------------------------------------------------------------------
        threading.Thread(target=self.hotkey, daemon=True).start()

        self.recordislive = False
        self.kill = False
        self.flag = False

        self.MainWindow.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.MainWindow.mainloop()
    def hotkey(self): #热键监听
         with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self,key): #热键处理
        try:
            if key == keyboard.Key.esc:
                self.flag=True
            elif key == keyboard.Key.space and not self.recordislive:
                self.start_record()
            elif key==keyboard.Key.up:
                self.StartSelectEnd=1
            elif key==keyboard.Key.down:
                self.EndSelectEnd=1
        except:
            pass
    def video_record(self):
            self.recordislive = True
            p = ImageGrab.grab((position1_x,position1_y,position2_x,position2_y))  # 获得当前屏幕
            screen_w, screen_h = p.size  # 获得当前屏幕的大小
            re = 10 - self.cb_resolution.current()  # 视频分辨率缩小
            out_w = int(screen_w * re / 10)
            out_h = int(screen_h * re / 10)
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 编码格式
            tempvideo = cv2.VideoWriter('~temp.mp4', fourcc, 20, (out_w, out_h))  # 输出文件命名为test.avi,帧率可以自己设置
            start_time = time.time()
            # int(self.cb_fps.get()[:-1])
            while True:
                im = ImageGrab.grab((position1_x, position1_y, position2_x, position2_y))
                im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)  # 转为opencv的BGR格式
                im = cv2.resize(im, (out_w, out_h), interpolation=cv2.INTER_AREA)
                tempvideo.write(im)
                if self.flag:
                    final_time = time.time()
                    tempvideo.release()
                    break
                if self.kill:
                    tempvideo.release()
                    self.deltempfile()
                    return

            if self.MainWindowisHide:
                self.MainWindow.update()
                self.MainWindow.deiconify()

            self.running.set('视频处理中，请稍候')
            tempvideo = cv2.VideoCapture('~temp.mp4')
            time_long = final_time - start_time
            fcount = tempvideo.get(cv2.CAP_PROP_FRAME_COUNT)
            sp = float(self.cb_speed.get()[:-1])  # 获得倍速数值
            fps = int(fcount / time_long * sp)  # 计算帧速度
            name = self.lb_save.cget('text')
            outvideo = cv2.VideoWriter(name, fourcc, fps, (out_w, out_h))
            while True:
                ret, frame = tempvideo.read()
                if not ret:
                    break
                outvideo.write(frame)
            tempvideo.release()
            outvideo.release()
            self.deltempfile()

            self.btn_start.configure(state=NORMAL)
            self.btn_stop.configure(state=DISABLED)
            self.btn_save.configure(state=NORMAL)
            self.cb_resolution.configure(state=NORMAL)
            self.cb_speed.configure(state=NORMAL)
            self.cb_fps.configure(state=NORMAL)
            self.cbtn_hide.configure(state=NORMAL)
            self.running.set('等待开始')

            self.recordislive = False

    def saveFile(self):  # 保存视频文件
        fn = asksaveasfilename(title='保存视频文件', defaultextension=".mp4", filetypes=[('视频文件', '*.mp4')])
        if fn != '':
            self.filename.set(fn)

    def on_closing(self):  # 关闭按钮
        if self.recordislive:
            ret = messagebox.askyesno('退出', '正在进行录屏中，是否退出？\n退出后将不能保存已录制内容！')
            if ret:
                self.kill = True
                self.MainWindow.destroy()
        else:
            self.MainWindow.destroy()

    def run_info(self):
        while True:
            for i in range(23):
                if self.flag:
                    return
                self.running.set('正在录制' + '.' * i)
                time.sleep(0.1)


    def SelectStartPoint(self):
        self.StartSelectEnd = 0
        global position1_x,position1_x
        messagebox.showinfo("起始点", "请把鼠标放到起始点,并按下PgUp")
        while(self.StartSelectEnd==0):
            time.sleep(1)
            position1_x, position1_y=pag.position()
            print("position1_x:")
            print(position1_x)

        messagebox.showinfo("终止点","请把鼠标放到终止点,并按下PgDn")
        time.sleep(1)
        global position2_x, position2_y
        while (self.EndSelectEnd == 0):
            time.sleep(1)
            position2_x, position2_y = pag.position()
            print("position2_x:")
            print(position2_x)
        img = ImageGrab.grab((position1_x,position1_y,position2_x,position2_y));
        img.show()
    def SelectEndPoint(self):
        global position2_x,position2_y
        position2_x,position2_y=pag.position()
    def ClearPoint(self):
        global position1_x,position1_y,position2_x,position2_y
        WholeScreen = ImageGrab.grab()
        position1_x = 0
        position1_y = 0
        position2_x, position2_y = WholeScreen.size
    def start_record(self):  # 录屏启动
        path = self.lb_save.cget('text')
        if path == '':
            messagebox.showerror('路径错误', '请先设置视频文件保存名称及路径！')
            return

        if os.path.exists(path):  # 如果文件存在
            ret = messagebox.askyesno('文件', '文件已经存在，是否覆盖？')
            if not ret:
                return

        self.flag = False

        threading.Thread(target=self.video_record).start()
        threading.Thread(target=self.run_info, daemon=True).start()

        if self.var_hide.get():
            self.MainWindow.withdraw()
            self.MainWindowisHide = True
        else:
            self.MainWindowisHide = False

        self.btn_start.configure(state=DISABLED)
        self.btn_stop.configure(state=NORMAL)
        self.btn_save.configure(state=DISABLED)
        self.cb_resolution.configure(state=DISABLED)
        self.cb_speed.configure(state=DISABLED)
        self.cb_fps.configure(state=DISABLED)
        self.cbtn_hide.configure(state=DISABLED)

    def stop_record(self):
        self.flag = True

    def deltempfile(self):
        path = '~temp.mp4'
        if os.path.exists(path):  # 如果文件存在
            os.remove(path)
if __name__ == '__main__':
    WholeScreen = ImageGrab.grab()
    position1_x = 0
    position1_y=0
    position2_x,position2_y = WholeScreen.size
    print(position2_y)
    app=App()

