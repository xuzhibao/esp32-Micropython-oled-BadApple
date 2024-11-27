# ESP32 MicroPython 0.96寸OLED屏幕播放《Bad Apple!!》 🎃📺

## 使用指南 🛠️：

1. **克隆或下载** 📥：从GitHub上克隆或下载并解压本仓库，使用Thonny IDE打开此目录。
2. **设备连接** 🔌：将你的ESP32开发板连接到电脑，并在Thonny中正确配置连接。
3. **文件上传** 📤：将`main.py`，`badapple.ebm`，以及`lib`文件夹上传至ESP32。
4. **屏幕连接** 🖥️：确保0.96寸OLED屏幕已正确连接至ESP32。如有需要，可以调整引脚定义以匹配实际连接。
5. **运行程序** 🚀：在Thonny中运行`main.py`，然后坐下来享受《Bad Apple!!》带来的视觉盛宴吧！
![连接图示例](https://raw.githubusercontent.com/xuzhibao/esp32-Micropython-oled-BadApple/refs/heads/main/Pictures/lianxian.png)
## 制作《Bad Apple!!》教程 📝：

本教程参考了[CSDN博客](https://blog.csdn.net/m0_47329175/article/details/130682985)的部分内容，适用于任何希望将视频转换为OLED屏幕可播放格式的项目。

### 准备工作 📁：

- 打开仓库目录，解压`source.zip`文件，其中包含：
  - `Bad Apple.mp4`（4K 60fps）
  - `Img2Lcd`文件夹（v4.0）
- 下载并安装[KMPlayer](https://dn.kmplayer.com/Dn/kmp32/2411/KMPlayer_4.2.3.19.exe)，用于视频捕捉。

### 捕捉视频帧 🎞️：

1. 使用KMPlayer打开`Bad Apple.mp4`，将视频暂停在起始位置。
2. 对画面右键选择“捕获”->“画面:高级捕获...”（或直接按Ctrl+G）。
   ![捕获设置](https://raw.githubusercontent.com/xuzhibao/esp32-Micropython-oled-BadApple/refs/heads/main/Pictures/buhuo.png)
3. 在`source`文件夹下创建`Pic`文件夹，根据图示设置参数后点击“开始”，并返回视频播放界面开始播放视频。完成后，你会在`/Source/Pic`文件夹中找到大约1900张图片，总计约46MB。
   ![捕获过程](https://raw.githubusercontent.com/xuzhibao/esp32-Micropython-oled-BadApple/refs/heads/main/Pictures/catch.png)

### 转换图片为二进制文件 🔄：

1. 打开`/Source/Img2lcd`文件夹中的`Img2Lcd.exe`，选择任意一张刚才捕获的图片，按图示设置参数。
   ![图片转换](https://raw.githubusercontent.com/xuzhibao/esp32-Micropython-oled-BadApple/refs/heads/main/Pictures/Image2.png)
2. 点击“批量转换”并确认。随后，在`/Source/Pic/batch`文件夹中执行如下命令以合并所有帧图片为一个二进制文件：
   ```bash
   copy /b *.ebm badapple.ebm
   ```
   这个`badapple.ebm`文件就是我们接下来要在ESP32上播放的文件啦！

### 编写并上传主程序 💻：

1. 打开Thonny，确保ESP32已连接且加载成功。
2. 将`badapple.ebm`文件上传至ESP32，并创建`lib`文件夹上传`ssd1306.py`驱动库（也可以先在本地创建`lib`文件夹，放入`ssd1306.py`后再整体上传）。
3. 接下来是编写主程序`main.py`，内容如下：

```python
# main.py

import machine
import ssd1306
import time
import os

# 初始化I2C和SSD1306
i2c = machine.I2C(0, scl=machine.Pin(4), sda=machine.Pin(5))  # 请根据实际连接调整引脚
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
```

4. 将`main.py`上传至ESP32，并通过Thonny运行它。现在，你可以看到OLED屏幕上开始播放《Bad Apple!!》了！

完成以上步骤，你就成功地在ESP32上实现了《Bad Apple!!》的播放！🎉
