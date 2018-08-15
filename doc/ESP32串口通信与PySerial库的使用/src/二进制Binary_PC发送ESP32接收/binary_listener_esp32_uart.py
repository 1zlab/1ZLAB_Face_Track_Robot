# -*- coding:utf-8 -*-
'''
## 功能描述
# 串口解析信息 二进制数据
## 接线：
# ESP32,TDX,D12 -> RXD,CP2102 (USB转TTL)
# ESP32,RXD,D13 -> TXD,CP2102 (USB转TTL)

# TODO 数据解析
# 运行过程中遭遇跳过 ？ ESP32的问题
'''
from machine import UART,Pin
import struct
import utime

uart = UART(2, baudrate=115200, rx=13,tx=12,timeout=10)


def depack_bin_data(byte_raw):
    '''
    将数据解包
        根据通信协议，解析数据， 并校验帧头
    '''
    FRAME_BYTE_LEN = 15

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



while True:
    if uart.any():
        print("Recv Raw Data")
        byte_raw = uart.readline()
        print(byte_raw)
        print(len(byte_raw))
        # 讲接收的字节流转换成容易读取的样式
        # byte_str = ':'.join(['{:02x}'.format(char_byte) for char_byte in byte_raw])
        try:
            (x, y,value) = depack_bin_data(byte_raw)
            print("x= %.2f y=%.2f value=%f"%(x, y, value))
        except ValueError as e:
            print(e)
        # print(byte_raw)
    # print('.')
    utime.sleep_ms(1000)

