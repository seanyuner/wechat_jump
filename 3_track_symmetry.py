'''
Bin Zhu @ 2018.01.08

**思路及说明**
1、注意到当前块和目标块的一定位置关系。
2、根据pixel值识别棋子。
3、本方案力求最简版，仅考虑x方向距离，且相关参数可能有待一步优化。
4、本代码试验机为1920*1080屏幕，实测距离时间系数一定随机性（1.5795情况下，或随机左偏越14个像素值或右偏7个）。

'''

import os
import time
import cv2
import random

# 截屏
def get_screenshot():
    os.system('adb shell screencap -p /sdcard/jump.png')
    os.system('adb pull /sdcard/jump.png')

# 寻找棋子位置，通过棋子最上一行pixel值判断
def find_loc(im, pixels_lim):
    min_w = 0
    min_h = 0
    max_h = 0
    w, h, _ = im.shape
    flag = False
    for j in range(int(w * 1/3), int(w * 2/3)):
        for i in range(int(h * 1/6), int(h * 5/6)):
            pixel = im[j, i]
            if pixels_lim[0] <= pixel[0] <= pixels_lim[1] and \
               pixels_lim[2] <= pixel[1] <= pixels_lim[3] and \
               pixels_lim[4] <= pixel[2] <= pixels_lim[5]:
                min_w = j
                min_h = i
                flag = True
                break
        if flag:
            break
    for i in range(int(h * 5/6), int(h * 1/6), -1):
        pixel = im[min_w, i]
        if pixels_lim[0] <= pixel[0] <= pixels_lim[1] and \
           pixels_lim[2] <= pixel[1] <= pixels_lim[3] and \
           pixels_lim[4] <= pixel[2] <= pixels_lim[5]:
            max_h = i
            break
    x = int((min_h + max_h) / 2)
    return x

# jump动作，触屏位置random一下，防ban
def jump(distance, coef_dis_time):
    press_time = int(distance * coef_dis_time)
    x = int(random.uniform(490, 590))
    y = int(random.uniform(1570, 1590))
    os.system('adb shell input swipe {} {} {} {} {}'.format(x, y, x, y, press_time))

# 主函数
def main():
    coef_dis_time = 1.5795                         # 距离时间系数
    chess_pixels = [55, 69, 49, 69, 45, 57]        # 识别棋子最上行的piexl值，依次为三个通道的上、下限
    distance = 453
    n = 1
    while True:
        n += 1
        time.sleep(random.uniform(0.9, 1.1))
        get_screenshot()
        im = cv2.imread('jump.png')
        chess_loc = find_loc(im, chess_pixels)
        print('jump {}\nchess location: {}\n'.format(n, chess_loc))
        distance = abs(1125 - chess_loc * 2)       # 当前块和目标块横向坐标和为1125像素值
        jump(distance, coef_dis_time)

if __name__ == '__main__':
    main()
