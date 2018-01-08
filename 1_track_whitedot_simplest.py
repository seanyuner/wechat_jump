'''
Bin Zhu @ 2018.01.08

**思路及说明**
1、注意到每次第一步距离为固定值，及将当前次命中中心后下一目标块出现的白点作为追踪目标，以此循环下去。
2、根据pixel值识别棋子和白点。
3、本方案力求最简版，仅考虑x方向距离，且相关参数可能有待一步优化。
4、本代码试验机为1920*1080屏幕，昨天还可达到300左右分数，今天只有几十了...（目测主要时间距离系数有待改进, random?）

'''

import os
import time
import cv2
import random

# 截屏
def get_screenshot():
    os.system('adb shell screencap -p /sdcard/jump.png')
    os.system('adb pull /sdcard/jump.png')

# 寻找棋子/白点的位置，通过棋子/白点最上一行pixel值判断
# 对于白点，设置为>=240比设置为==245更好，在某次没有命中时，若目标块有对称白色可补救一次
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
    os.system('adb shell input swipe {} {} {} {} {}'.format(*[x, y, x, y, press_time]))

# 主函数
def main():
    coef_dis_time = 1.595                          # 距离和触屏时间之间的系数
    chess_pixels = [54, 76, 47, 60, 38, 61]        # 识别棋子最上行的piexl值，依次为三个通道的上、下限
    dot_pixels = [230, 255, 230, 255, 230, 255]    # 识别白点最上行的pixel值，三个通道的上下限相同
    distance = 453                                 # 手动设置第一跳
    jump(distance, coef_dis_time)
    n = 1                                          # 计数
    while True:
        n += 1
        time.sleep(random.uniform(0.9, 1.1))
        get_screenshot()
        im = cv2.imread('jump.png')
        chess_loc = find_loc(im, chess_pixels)
        dot_loc = find_loc(im, dot_pixels)
        print('jump {}\nchess location: {}\ndot location: {}\n'.format(n, chess_loc, dot_loc))
        distance = abs(chess_loc - dot_loc)
        jump(distance, coef_dis_time)

if __name__ == '__main__':
    main()
