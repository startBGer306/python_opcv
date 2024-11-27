import cv2
import serial as serial
import time

if __name__=="__main__":
    ser=serial.Serial("COM8",115200)
    data_a=1
    data_b=321
    data_c=126
    data_d=0
    data_e=2
    data_head= 0xAA
    data_end=0xff
    while True:
        # byte_data_head = data_head.to_bytes(1, byteorder='big', signed=False)
        # byte_data_a=data_a.to_bytes(1, byteorder='big', signed=False)
        # byte_data_b=data_b.to_bytes(2, byteorder='big', signed=False)
        # byte_data_c=data_c.to_bytes(2, byteorder='big', signed=False)
        # byte_data_end=data_end.to_bytes(1, byteorder='big', signed=False)
        # ser.write(byte_data_head)
        # ser.write(byte_data_a)
        # ser.write(byte_data_b)
        # ser.write(byte_data_c)
        # ser.write(byte_data_end)
        # time.sleep(1)
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)  # 读取所有可用的数据
            print(f"接收到的数据: {data}")

            # 将每个字节转换为对应的字符
            char_list = []
            for byte in data:
                if 1 <= byte <= 6:
                    char = chr(ord('1') + (byte - 1))  # 将字节值转换为字符 '1' 到 '6'
                    char_list.append(char)
                else:
                    char_list.append('?')  # 处理无效字节

            char_string = ''.join(char_list)
            print(f"转换后的字符信息: {char_string}")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
