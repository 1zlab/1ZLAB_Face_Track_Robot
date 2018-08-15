# -*- coding:utf-8 -*-

def verify_data(byte_buffer, new_byte):
    # 校验
    veri_code = bytearray(b'\xaa\xae')
    # 校验字节长度
    veri_code_len = len(veri_code)

    byte_buffer.append(new_byte[0])
    while len(byte_buffer) > veri_code_len:
        byte_buffer.pop()
    
    if len(byte_buffer) < veri_code_len:
        # 长度不足
        return False
    
    # print(veri_code)
    # print(byte_buffer)

    return veri_code == byte_buffer


print(verify_data(bytearray(b'\xaa'),b'\xae'))