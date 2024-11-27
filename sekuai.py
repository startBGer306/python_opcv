import tkinter as tk
import cv2
import numpy as np

def morphological_operations(mask):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    return closing
class HSVControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HSV Color Control")

        # 创建滑动条
        self.h_low = tk.Scale(root, from_=0, to=180, label='H Low 0', orient='horizontal', length=300)
        self.s_low = tk.Scale(root, from_=0, to=255, label='S Low 0', orient='horizontal', length=300)
        self.v_low = tk.Scale(root, from_=0, to=255, label='V Low 0', orient='horizontal', length=300)
        self.h_high = tk.Scale(root, from_=0, to=180, label='H High 0', orient='horizontal', length=300)
        self.s_high = tk.Scale(root, from_=0, to=255, label='S High 0', orient='horizontal', length=300)
        self.v_high = tk.Scale(root, from_=0, to=255, label='V High 0', orient='horizontal', length=300)
        # self.h_low1 = tk.Scale(root, from_=0, to=180, label='H Low 1', orient='horizontal', length=300)
        # self.s_low1= tk.Scale(root, from_=0, to=255, label='S Low 1', orient='horizontal', length=300)
        # self.v_low1 = tk.Scale(root, from_=0, to=255, label='V Low 1', orient='horizontal', length=300)
        # self.h_high1 = tk.Scale(root, from_=0, to=180, label='H High 1', orient='horizontal', length=300)
        # self.s_high1 = tk.Scale(root, from_=0, to=255, label='S High 1', orient='horizontal', length=300)
        # self.v_high1 = tk.Scale(root, from_=0, to=255, label='V High 1', orient='horizontal', length=300)

        # 设置初始值
        self.h_low.set(0)
        self.s_low.set(0)
        self.v_low.set(0)
        self.h_high.set(255)
        self.s_high.set(255)
        self.v_high.set(255)
        # self.h_low1.set(0)
        # self.s_low1.set(0)
        # self.v_low1.set(0)
        # self.h_high1.set(255)
        # self.s_high1.set(255)
        # self.v_high1.set(255)

        # 布局滑动条
        self.h_low.pack()
        self.s_low.pack()
        self.v_low.pack()
        self.h_high.pack()
        self.s_high.pack()
        self.v_high.pack()
        # self.h_low1.pack()
        # self.s_low1.pack()
        # self.v_low1.pack()
        # self.h_high1.pack()
        # self.s_high1.pack()
        # self.v_high1.pack()

        # 创建摄像头对象
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.camera.set(cv2.CAP_PROP_FPS, 30)

        # 检查摄像头是否打开
        if not self.camera.isOpened():
            print("no camera")
            return

        # 开始视频处理
        self.update_frame()

    def update_frame(self):
        # 获取帧
        ret, frame = self.camera.read()
        if not ret:
            print("no frame")
            self.root.after(10, self.update_frame)
            return

        # 从滑动条获取当前值
        h_low = self.h_low.get()
        s_low = self.s_low.get()
        v_low = self.v_low.get()
        h_high = self.h_high.get()
        s_high = self.s_high.get()
        v_high = self.v_high.get()
        # h_low1 = self.h_low1.get()
        # s_low1 = self.s_low1.get()
        # v_low1 = self.v_low1.get()
        # h_high1= self.h_high1.get()
        # s_high1 = self.s_high1.get()
        # v_high1 = self.v_high1.get()

        # 定义两个颜色范围
        lower_1 = np.array([h_low, s_low, v_low])
        upper_1 = np.array([h_high, s_high, v_high])
        # lower_2 = np.array([h_low1, s_low1, v_low1])  # 考虑到红色跨越0度和180度的情况
        # upper_2 = np.array([ h_high1, s_high1, v_high1])
      

        # 处理色块
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv_frame, lower_1, upper_1)
        # mask2 = cv2.inRange(hsv_frame, lower_2, upper_2)
        # mask = cv2.bitwise_or(mask1, mask2)
       

        # 显示结果
        cv2.imshow("mask", mask1)
        cv2.imshow("farme",frame)

        # 继续更新帧
        self.root.after(10, self.update_frame)

    def close_camera(self):
        self.camera.release()
        cv2.destroyAllWindows()
        self.root.quit()
if __name__ == "__main__":
    root = tk.Tk()
    app = HSVControlApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_camera)  # 关闭窗口时释放摄像头
    root.mainloop()