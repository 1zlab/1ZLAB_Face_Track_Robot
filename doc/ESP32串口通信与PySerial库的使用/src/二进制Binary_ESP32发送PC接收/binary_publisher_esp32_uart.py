'''
串口发送信息 二进制数据
接线：
    ESP32,TDX,D12 -> RXD,CP2102 (USB转TTL)
    ESP32,RXD,D13 -> TXD,CP2102 (USB转TTL)
'''

from machine import UART,Pin
import struct
import utime


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

try:
    while True:
        # print(uart)
        uart.write(pack_bin_data(x, y, value))
        utime.sleep_ms(1000)
except:
    print("程序意外终端， Bye")