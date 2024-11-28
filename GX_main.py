import cv2
import numpy as np
import threading
import serial
import time
#****************************************************************************************************#
# 初始化摄像头
def init_camera():
    global camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not camera.isOpened():
        print("Error: no camera")
        return False
    return True
#****************************************************************************************************#
# 通用颜色检测函数
def detect_color(stop_event, min_area, lower_bounds, upper_bounds, color_id):
    global camera
    while not stop_event.is_set():
        ret, img = camera.read()
        if not ret:
            continue
        frame = img.copy()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        combined_mask = cv2.inRange(hsv_frame, lower_bounds, upper_bounds)
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #初始化变量，用于输出000
        found_contour=False

        if contours:
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    circle_x = int(x + w / 2)
                    circle_y = int(y + h / 2)
                    datatransfrom(color_id, circle_x, circle_y)
                    found_contour=True
                    break
        if not found_contour:
            datatransfrom(0, 640, 360)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
#****************************************************************************************************#
# 红色专属检测函数
def detect_color_red(stop_event, min_area, lower_bounds, upper_bounds, color_id):
    global camera
    while not stop_event.is_set():
        ret, img = camera.read()
        if not ret:
            continue
        frame = img.copy()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_0 = cv2.inRange(hsv_frame, lower_bounds, upper_bounds)
        mask_1=cv2.inRange(hsv_frame,np.array([139, 76, 76]), np.array([180, 255, 255]))
        combined_mask=cv2.bitwise_or(mask_0,mask_1)
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #初始化变量，用于输出000
        found_contour=False

        if contours:
            print(contours)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    circle_x = int(x + w / 2)
                    circle_y = int(y + h / 2)
                    datatransfrom(color_id, circle_x, circle_y)
                    found_contour=True
                    break
        if not found_contour:
            datatransfrom(0,640,360)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
#****************************************************************************************************#
# 通用圆形检测函数
def detect_circle(stop_event, min_area, lower_bounds, upper_bounds, color_id):
    global camera
    while not stop_event.is_set():
        ret, img = camera.read()
        if not ret:
            continue
        frame = img.copy()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        combined_mask = cv2.inRange(hsv_frame, lower_bounds, upper_bounds)
        circles = cv2.HoughCircles(combined_mask, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=55, minRadius=30, maxRadius=min_area)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            max_radius=0
            max_circle=None
            for i in circles[0,:]:
                if i[2]>max_radius:
                    max_circle=i
                    max_radius=i[2]
            if max_circle is not None:
                center = [int(max_circle[0]), int(max_circle[1])]
                datatransfrom(color_id, center[0], center[1])
        else:
            datatransfrom(0, 640, 360)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
#****************************************************************************************************#
# 红色圆环专属检测函数
def detect_circle_red(stop_event, min_area, lower_bounds, upper_bounds, color_id):
    global camera
    while not stop_event.is_set():
        ret, img = camera.read()
        if not ret:
            continue
        frame = img.copy()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_0 = cv2.inRange(hsv_frame, lower_bounds, upper_bounds)
        mask_1=cv2.inRange(hsv_frame,np.array([139, 76, 76]), np.array([180, 255, 255]))
        combined_mask=cv2.bitwise_or(mask_0,mask_1)
        circles = cv2.HoughCircles(combined_mask, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=55, minRadius=30, maxRadius=min_area)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            max_radius=0
            max_circle=None
            for i in circles[0,:]:
                if i[2]>max_radius:
                    max_circle=i
                    max_radius=i[2]
            if max_circle is not None:
                center = [int(max_circle[0]), int(max_circle[1])]
                datatransfrom(color_id, center[0], center[1])
        else:
            datatransfrom(0, 640, 360)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
#****************************************************************************************************#
def Det_all(stop_event,min_area):
    global camera
    while not stop_event.is_set():
        ret,img=camera.read()
        if not ret:
            continue
        frame=img.copy()
        hsv_frame =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #****************************************************************************************************#
        #red块 
        all_red_mask1 = cv2.inRange(hsv_frame,np.array([0, 95, 132]), np.array([37, 255, 255]))
        all_red_mask2 = cv2.inRange(hsv_frame,np.array([139, 76, 76]), np.array([180, 255, 255]))
        all_red_mask =cv2.bitwise_or(all_red_mask1,all_red_mask2)
        contours_all_red, _ = cv2.findContours(all_red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #****************************************************************************************************#
        #green块 
        all_green_mask =cv2.inRange(hsv_frame,np.array([35, 52, 99]), np.array([93, 255, 255]))
        contours_all_green, _ = cv2.findContours(all_green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #****************************************************************************************************#
        #blue块 
        all_blue_mask =cv2.inRange(hsv_frame,np.array([95, 70, 64]), np.array([154, 255, 255]))
        contours_all_blue, _ = cv2.findContours(all_blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #初始化变量，用于输出000
        found_contour=False

        det_for(contours_all_red,min_area,1,found_contour)
        time.sleep(0.005)
        det_for(contours_all_green,min_area,2,found_contour)
        time.sleep(0.005)
        det_for(contours_all_blue,min_area,3,found_contour)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#****************************************************************************************************#
def Donothing(stop_event):
    while not stop_event.is_set():
        print("Do Nothing")
        datatransfrom(8,640,360)
        time.sleep(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
#****************************************************************************************************#
# 数据标准化转化传输函数
def datatransfrom(exist, x_o, y_o):
    x = x_o - 640
    y = 360 - y_o
    data_head = 0xaa
    data_end = 0xff
    data_head_byte = data_head.to_bytes(1, byteorder='big', signed=False)
    data_end_byte = data_end.to_bytes(1, byteorder='big', signed=False)
    exist_byte = exist.to_bytes(1, byteorder='big', signed=False)
    center_x_byte = x.to_bytes(2, byteorder='big', signed=True)
    center_y_byte = y.to_bytes(2, byteorder='big', signed=True)
    data = b"".join([data_head_byte, exist_byte, center_x_byte, center_y_byte, data_end_byte])
    listener.ser.write(data)
#****************************************************************************************************#
# 物块防止台检测判断函数
def det_for(contours,min_area,color_id,found_contour):
    if contours:
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    circle_x = int(x + w / 2)
                    circle_y = int(y + h / 2)
                    datatransfrom(color_id, circle_x, circle_y)
                    found_contour=True
                    break
    if not found_contour:
            datatransfrom(0, 640, 360)
#****************************************************************************************************#
# 串口线程管理类
class SerialListener(threading.Thread):
    def __init__(self, port, baudrate=115200):
        super(SerialListener, self).__init__()
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.stop_event = threading.Event()
        self.task = None

    def open_serial(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"串口 {self.port} 打开成功")
        except serial.SerialException as e:
            print(f"串口 {self.port} 打开失败: {e}")
            self.ser = None

    def run(self):
        self.open_serial()
        if self.ser is None:
            return
        print(f"开始监听 {self.port}...")
        while not self.stop_event.is_set():
            if self.ser.in_waiting > 0:
                data_o = self.ser.read(self.ser.in_waiting)
                # 将每个字节转换为对应的字符
                char_list = []
                for byte in data_o:
                    if 1 <= byte <= 8:
                        char = chr(ord('1') + (byte - 1))  # 将字节值转换为字符 '1' 到 '8'
                        char_list.append(char)
                    else:
                        char_list.append('?')  # 处理无效字节

                data = ''.join(char_list)
                print(f"转换后的字符信息: {data}")
                if data in ["1", "2", "3", "4", "5", "6","7","8"]:
                    self.task = data

    def stop(self):
        print("停止监听...")
        self.stop_event.set()
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("串口已关闭")
#****************************************************************************************************#
# 主函数
if __name__ == "__main__":
    # 初始化摄像头
    if init_camera():
        print("摄像头已经开始工作")
    else:
        print("摄像头未正常打开")
    
    # 创建并启动串口监听线程
    listener = SerialListener(port="COM7")  # 根据实际情况修改端口号
    listener.start()
    
    # 初始化线程任务变量
    current_task = None
    image_threads = []
    stop_event = threading.Event()
    
    try:
        while True:
            if listener.task != current_task:
                current_task = listener.task
                stop_event.set()
                # 停止所有现有线程
                for thread in image_threads:
                    thread.join()
                image_threads.clear()
                stop_event.clear()
                
                if current_task == "1":
                    thread = threading.Thread(target=detect_color_red, args=(stop_event, 100*100, np.array([0, 95, 132]), np.array([37, 255, 255]), 1))
                    image_threads.append(thread)
                    thread.start()
                elif current_task == "2":
                    thread = threading.Thread(target=detect_color, args=(stop_event, 100*100, np.array([35, 52, 99]), np.array([93, 255, 255]), 2))
                    image_threads.append(thread)
                    thread.start()
                elif current_task == "3":
                    thread = threading.Thread(target=detect_color, args=(stop_event, 100*100, np.array([95, 70, 64]), np.array([154, 255, 255]), 3))
                    image_threads.append(thread)
                    thread.start()
                elif current_task == "4":
                    thread = threading.Thread(target=detect_circle_red, args=(stop_event, 200, np.array([0, 95, 132]), np.array([37, 255, 255]), 4))
                    image_threads.append(thread)
                    thread.start()
                elif current_task == "5":
                    thread = threading.Thread(target=detect_circle, args=(stop_event, 200, np.array([35, 52, 99]), np.array([93, 255, 255]), 5))
                    image_threads.append(thread)
                    thread.start()
                elif current_task == "6":
                    thread = threading.Thread(target=detect_circle, args=(stop_event, 200, np.array([95, 70, 64]), np.array([154, 255, 255]), 6))
                    image_threads.append(thread)
                    thread.start()
                elif current_task == "7":
                    thread = threading.Thread(target=Det_all, args=(stop_event, 100*100,))
                    image_threads.append(thread)
                    thread.start()
                elif current_task == "8":
                    thread = threading.Thread(target=Donothing, args=(stop_event,))
                    image_threads.append(thread)
                    thread.start()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        stop_event.set()
        for thread in image_threads:
            thread.join()
        listener.stop()
        camera.release()
        cv2.destroyAllWindows()