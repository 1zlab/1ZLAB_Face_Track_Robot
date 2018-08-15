# -*- coding:utf-8 -*-
'''
PC使用PySerial发送数据

## 注意
运行此程序的时候，需要修改设备的权限，
sudo chmod 777 /dev/ttyUSB?  ，其中 ? = 0,1,2,...
或者使用管理员权限运行脚本
sudo python xxxxx.py

'''
import serial
import struct
import time

# 串口号 默认为 /dev/ttyUSB0
ser_dev = '/dev/ttyUSB1'
# 创建一个串口实例
ser = serial.Serial(ser_dev,115200, timeout=1, bytesize=8)


def pack_bin_data(x,y,value):
    '''
    h: unsigned short bit=2
    b: unsigned char (byte): bit =1
    i: integer bit=4
    f: float bit=4

    b*2 + i*2 + f*1
    = 1*3 + 4*2 + 4*1 = 15byte

    '''

    bin_data = struct.pack(">BBiifB",
        0xAA,
        0xAE,
        int(x * 100), # x坐标，精确到小数点后两位
        int(y * 100 ), # y坐标，精确到小数点后两位
        float(value), # 传感器读入的值，float类型
        0x0A) # 结束符 '\n = 0x0A
    return bin_data

x = 100.123
y = -23.398
value = 1.2912312352

byte_raw = pack_bin_data(x,y,value)

while True:
    ser.write(byte_raw)
    # ser.write(b'\xAA')
    # ser.write('haha')
    # 讲接收的字节流转换成容易读取的样式
    byte_str = ':'.join(["{:02x}".format(char_byte) for char_byte in bytearray(byte_raw)])
    # 打印原始的字节数据()
    print("Send字节流: "+byte_str+"\n")

    # 每隔10s发送一次数据
    time.sleep(3)
