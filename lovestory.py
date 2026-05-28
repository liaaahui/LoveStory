#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
from PIL import Image
from waveshare_epd import epd7in5b_V2

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in5b_V2 - Loop pictures 1.bmp to 523.bmp, each 5s, red layer empty")
    epd = epd7in5b_V2.EPD()
    epd.init()
    epd.Clear()

    # 收集 1.bmp ~ 523.bmp 中存在的文件
    picture_files = []
    for i in range(1, 524):
        filename = f"{i}.bmp"
        filepath = os.path.join(picdir, filename)
        if os.path.exists(filepath):
            picture_files.append(filepath)
        else:
            logging.warning(f"File {filename} not found, skip")

    if not picture_files:
        logging.warning("No valid picture files (1.bmp..523.bmp) found.")
    else:
        for img_path in picture_files:
            logging.info(f"Displaying: {os.path.basename(img_path)}")
            # 打开黑白图层
            black_img = Image.open(img_path)
            # 创建与黑白图层相同尺寸的全白图像（1位色，255表示白色）
            white_img = Image.new('1', black_img.size, 255)
            # 显示：黑色图层使用图片内容，红色图层全白（无红色）
            epd.display(epd.getbuffer(black_img), epd.getbuffer(white_img))
            time.sleep(5)            # 每张显示5秒

    logging.info("Clear...")
    epd.init()
    epd.Clear()
    logging.info("Goto Sleep...")
    epd.sleep()

except IOError as e:
    logging.info(e)
except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5b_V2.epdconfig.module_exit(cleanup=True)
    exit()