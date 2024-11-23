import machine
import ssd1306
import time
import os

# 初始化I2C和SSD1306
i2c = machine.I2C(0, scl=machine.Pin(4), sda=machine.Pin(5))  # 根据你的连接调整引脚
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def display_frame(frame_data):
    """显示一帧图像"""
    for y in range(0, 64):
        for x in range(0, 128):
            # 计算字节和位
            byte_index = (y * 128 + x) // 8
            bit_index = x % 8
            # 获取像素值（1或0）
            pixel = (frame_data[byte_index] >> (7 - bit_index)) & 1
            # 设置OLED像素
            oled.pixel(x, y, pixel)
    oled.show()

def play_badapple():
    """播放Bad Apple动画"""
    frame_size = 1024
    frame_data = bytearray(frame_size)
    frame_index = 0
    
    # 打开文件
    with open('badapple.ebm', 'rb') as f:
        while True:
            # 读取一帧数据
            bytes_read = f.readinto(frame_data)
            if bytes_read < frame_size:
                # 如果读取的字节少于1024，重置文件指针
                f.seek(0)
                continue
            
            # 显示当前帧
            display_frame(frame_data)
            time.sleep(0.01)  # 延迟10毫秒

# 启动播放
play_badapple()
