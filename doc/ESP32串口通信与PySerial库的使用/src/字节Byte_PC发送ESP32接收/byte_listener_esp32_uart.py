# -*- coding:utf-8 -*-
'''
串口发送信息 （字符chuan）
接线：
    ESP32,TDX,D12 -> RXD,CP2102 (USB转TTL)
    ESP32,RXD,D13 -> TXD,CP2102 (USB转TTL)

TODO 信息丢失或者损坏
栈不够用等一系列问题

TODO byte解码问题， 失败
'''

from machine import UART,Pin
import utime

# 初始化串口 UART
# 波特率 115200
# rx -> Pin 13
# tx -> Pin 12

# 注意，我们这里拓展了buffer的尺寸
uart = UART(2, baudrate=115200, rx=13,tx=12,timeout=10)
# 注意 buffer_size暂时还不支持
# uart = UART(2, baudrate=115200, bits=8, parity=0, rx=13,tx=12,buffer_size=4096，timeout=10)

while True:
    if uart.any():
        # 如果有数据的话， 就读入一行
        info_byte = uart.readline()
        print(info_byte)
        # info_str = info_byte.decode('uft8')
        # print(info_str)

        # Unicode  Error
        # info_str = info_byte.decode('ascii')
        
        # not Implement 没有实现这个功能
        # info_str = str(info_byte,encoding="ascii")
        
        # print(info_byte.decode(encoding="ascii"))
    # 时间间隔1s
    utime.sleep_ms(100)