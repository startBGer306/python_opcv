import cv2
import numpy as np
import time

# 初始化摄像头
def init_camera():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.set(cv2.CAP_PROP_FPS, 30)
    
    if not camera.isOpened():
        print("Error: no camera")
        return None
    
    # 增加初始化后的延迟
    time.sleep(2)
    return camera

# 形态学操作
def morphological_operations(mask):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    return closing

# 检测红色圆环并标记中心坐标
def detect_red_circle(camera):
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error: can't catch frame")
            break

        # 读取图像
        ret,frame=camera.read()
        # 转换为HSV颜色空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 定义红色的HSV范围
        lower_red1 = np.array([0, 95, 132])
        upper_red1 = np.array([69, 255, 255])
        lower_red2 = np.array([139, 78, 72])
        upper_red2 = np.array([180, 255, 255])

        # 创建掩码
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        # 对掩码进行形态学操作，去除噪声
        mask_c = morphological_operations(mask)

        # 将掩码应用于原始图像
        red_only = cv2.bitwise_and(frame, frame, mask=mask)

        # 转换为灰度图像
        gray = cv2.cvtColor(red_only, cv2.COLOR_BGR2GRAY)

        # 高斯模糊
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        # 边缘检测
        edges = cv2.Canny(blurred, 50, 150)

        # 霍夫圆变换
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=50,param1=100, param2=55, minRadius=50, maxRadius=0)

        max_radius = 0
        max_center = None

        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # 过滤掉面积小于 100 * 100 的圆
                if i[2] ** 2 >= 200 & i[2]**2<1000:
                    if i[2] > max_radius:
                        max_radius = i[2]
                        max_center = (i[0], i[1])

            if max_center and max_radius:
                # 绘制最大圆和中心点
                cv2.circle(frame, max_center, max_radius, (0, 255, 0), 2)
                cv2.circle(frame, max_center, 5, (0, 0, 255), -1)
                # 显示中心坐标
                cv2.putText(frame, f"({max_center[0]}, {max_center[1]})", (max_center[0] + 10, max_center[1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        # 显示结果
        cv2.imshow("Red Circle Detection",mask_c)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 主函数
if __name__ == "__main__":
    camera = init_camera()
    if camera is None:
        exit(1)
    
    try:
        detect_red_circle(camera)
    except KeyboardInterrupt:
        print("程序已退出")
    
    # 释放资源
    camera.release()
    cv2.destroyAllWindows()