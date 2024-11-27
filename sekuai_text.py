import cv2
import numpy as np
# 测试函数

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera.set(cv2.CAP_PROP_FPS, 30)

while True:
    # 获取摄像头每帧
    ret, img = camera.read()
    if not ret:
        print("Failed to grab frame")
        break
    frame = img.copy()

    # 获取蒙版
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue0 = np.array([95, 70, 64])
    upper_blue0 = np.array([154, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, lower_blue0, upper_blue0)

    # 检测圆
    circles = cv2.HoughCircles(blue_mask, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=55, minRadius=30, maxRadius=200)
    
    x=None
    y=None
    if circles is not None:
        circles = np.uint16(np.around(circles))
        #找最大圆
        max_radius=0
        max_circle=None
        for i in circles[0,:]:
            if i[2]>max_radius:
                max_circle = i
                max_radius = i[2]
        if max_circle is not None:
            center = [int(max_circle[0]),int(max_circle[1])]
            radius=max_radius
            #绘制，注意上方center已改为元组非向量下面注释代码可能报错
            cv2.circle(frame,tuple(center),radius,(255,255,255),2)
            cv2.circle(frame,tuple(center),1,(255,255,255),-1)
            x=center[0]-640
            y=360 - center[1]
    #cv2.imshow("frame",frame)
    #cv2.imshow("mask", blue_mask)
    print((x,y))
    #退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
