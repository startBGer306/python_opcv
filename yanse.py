import cv2
import numpy as np


#***************************************************************************************#
#函数用来测试搜索图像中相关颜色
def detect_red_objects(image_path):
    # 读取图片
    image = cv2.imread(image_path)
    
    # 检查图片是否成功读取
    if image is None:
        print("Error: 图片未找到或无法读取，请检查路径。")
        return
    
    # 将BGR图像转换到HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 定义红色范围
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    
    # 创建红色的掩码
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    # 寻找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 遍历所有的轮廓
    for contour in contours:
        # 计算轮廓的边界框
        x, y, w, h = cv2.boundingRect(contour)
        
        # 绘制白色矩形边框
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 2)
    
    # 显示结果
    cv2.imshow('Red Objects Detected', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#***************************************************************************************#
detect_red_objects("D:\DES\pcture\wuliao.jpg")