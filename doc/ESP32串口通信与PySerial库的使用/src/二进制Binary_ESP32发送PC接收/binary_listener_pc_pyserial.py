# -*- coding:utf-8 -*-
'''
PC上使用PySerial解析二进制数据

## 注意
运行此程序的时候，需要修改设备的权限，
sudo chmod 777 /dev/ttyUSB?  ，其中 ? = 0,1,2,...
或者使用管理员权限运行脚本
sudo python xxxxx.py


## 样例输出
Recv字节流: aa:ae:00:00:27:1c:ff:ff:f6:dd:3f:a5:47:11:0a
数据解析: x= 100.00, y= -24.00, value=1.291231

'''

import serial
import struct
# 串口号 默认为 /dev/ttyUSB0
ser_dev = '/dev/ttyUSB1'


FRAME_BYTE_LEN = 15 # 通信协议里面每一帧字节的长度

def depack_bin_data(byte_raw):
    '''
    将数据解包
        根据通信协议，解析数据， 并校验帧头
    '''
    global FRAME_BYTE_LEN

    if len(byte_raw) != FRAME_BYTE_LEN:
        # 检查数据帧长度是否满足条件
        raise ValueError("ERROR: 长度不满足条件")
    
    (verify_byte1, verify_byte2, x, y, value, _) = struct.unpack('>BBiifB', byte_raw)
    if verify_byte1 == 0xAA and verify_byte2 == 0xAE:
        x /= 100 # 恢复为实际数值范围
        y /= 100 # 恢复为实际数值范围
        return (x, y, value)
    else:
        raise ValueError("ERROR: 数据帧头校验失败")

# 创建一个串口实例
ser = serial.Serial(ser_dev,115200, timeout=1, bytesize=8)

while True:
    # 读取的是byte类型 ，例如
    #　b'hello\n'
    # ser.read() # 注意：串口读取单个字节 (一个字节是16位)
    # ser.read(n) # 读入N个字节 
    # print(ser.read())
    
    # 读入一行数据  以EOF标识(\n)作为参考
    byte_raw = ser.readline()
    # 讲接收的字节流转换成容易读取的样式
    byte_str = ':'.join(["{:02x}".format(char_byte) for char_byte in bytearray(byte_raw)])
    # 打印原始的字节数据()
    print("Recv字节流: "+byte_str)


    try:
        # 读取解析的数据
        x,y,value = depack_bin_data(byte_raw)
        print("数据解析: "+"x= %.2f, y= %.2f, value=%f\n"%(x, y, value))
    
    except ValueError as e:
        # 若帧头不匹配
        print(e)