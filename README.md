# ESP32 micropython 0.96寸oled屏幕播放Bad Apple！！

## 食用方法：

1.clone或者下载并解压本仓库，使用Tonny打开此目录

2.将你的ESP32连接到你的电脑，并在Tonny中加载

3.将main.py，badapple.ebm，和lib文件夹上传到ESP32上

4.连接好0.96寸oled屏幕到esp32（可选：修改引脚定义）

5.运行main.py，然后开始享受你的Bad Apple！！



## 以下为制作Bad Apple教程，同样适用于其他视频：

本教程部分参考：[0.96寸oled显示坏苹果(badapple)_0.96寸oled显示动画视频 bad apple代码-CSDN博客](https://blog.csdn.net/m0_47329175/article/details/130682985)

打开仓库目录，解压source.7z文件，包含以下内容：

> 1.Bad Apple.mp4(4K 60fps)
>
> 2.Img2Lcd文件夹(v4.0)

在开始之前还需要下载安装[KMPlayer](https://dn.kmplayer.com/Dn/kmp32/2411/KMPlayer_4.2.3.19.exe)


### 正文：

使用KMPlayer打开Bad Apple.mp4，将视频暂停在最开始

对画面右键->捕获->画面:高级捕获..(或者按下键盘上的Ctrl+G)
![](https://raw.githubusercontent.com/xuzhibao/esp32-Micropython-oled-BadApple/refs/heads/main/Pictures/buhuo.png)

可以在source文件夹下新建Pic文件夹，并按照图示进行设置：

![](https://raw.githubusercontent.com/xuzhibao/esp32-Micropython-oled-BadApple/refs/heads/main/Pictures/catch.png)

点击开始，并回到视频中开始播放视频，等待播放完成后会在/Source/Pic文件夹下生成制作视频所需的帧图片(约1900张图片，总大小约为46M)
打开/Source/Img2lcd文件夹，打开Img2Lcd.exe，打开任意一张刚才捕获的图片之一，按照如图进行设置

![](https://raw.githubusercontent.com/xuzhibao/esp32-Micropython-oled-BadApple/refs/heads/main/Pictures/Image2.png).

然后点击批量转换并确定，之后会发现/Source/Pic下生成了一个batch文件夹，进入此文件夹并在终端(或者CMD)中打开输入:
  ```bash
copy  /b  *.ebm  badapple.ebm
  ```
回车确定，会在batch文件夹下新生成一个badapple.ebm，此二进制文件就是接下来要上传到ESP32中使用oled屏幕播放的文件

打开Thonny，连接好esp32并加载

上传badapple.ebm，同时在ESP32上新建文件夹lib上传ssd1306.py(你也可以先在电脑上的资源管理器新建lib文件夹把ssd1306.py库放进去之后将lib文件夹整个使用Thonny上传到ESP32)

接下来就是编写主程序

```python
#main.py

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
    with open('badapple2.ebm', 'rb') as f:
        while True:
            # 读取一帧数据
            bytes_read = f.readinto(frame_data)
            if bytes_read < frame_size:
                # 如果读取的字节少于1024，重置文件指针
                f.seek(0)
                continue
            
            # 显示当前帧
            display_frame(frame_data)
            time.sleep(0.01)  # 延10毫秒

# 启动播放
play_badapple()

```
将main.py上传到ESP32中并运行
至此，你已经完成的所有内容！！
