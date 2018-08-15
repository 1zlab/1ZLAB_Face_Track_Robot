# -*- coding:utf-8 -*-
'''
## 功能描述
# 串口解析信息 二进制数据
## 接线：
# ESP32,TDX,D13 ->ESP32,RXD,D12
'''
from machine import UART,Pin
import struct
import utime
# 初始化串口 UART
# 波特率 115200
# rx -> Pin 13
# tx -> Pin 12

uart = UART(2, baudrate=115200, rx=13,tx=12,timeout=10)

def pack_bin_data(x,y,value):
    '''
    h: unsigned short bit=2
    b: unsigned char (byte): bit =1
    i: integer bit=4
    f: float bit=4

    b*2 + i*2 + f*1
    = 1*2 + 4*2 + 4*1 = 14byte

    '''
    bin_data = struct.pack(">BBiifB",
        0xAA,
        0xAE,
        int(x * 100), # x坐标，精确到小数点后两位
        int(y * 100 ), # y坐标，精确到小数点后两位
        float(value), # 传感器读入的值，float类型
        0x0A) # 结束符 \n = 0x0A
    print(bin_data)
    return bin_data

x = 100.123
y = -23.398
value = 1.2912312352

while True:
    print('Send Data')
    print(pack_bin_data(x, y, value))
    uart.write(pack_bin_data(x, y, value))
    utime.sleep_ms(1000)
    print("Recv Data")
    # byte_raw = uart.readline()
    byte_raw = uart.read()
    print(len(byte_raw))
    print(byte_raw)
    # 讲接收的字节流转换成容易读取的样式
    # byte_str = ':'.join(["{:02x}".format(char_byte) for char_byte in byte_raw])
    # print(byte_str)
    # print(byte_raw)
    utime.sleep_ms(1000)
