import os
import time
import cv2
import random

def get_screenshot():
    os.system('adb shell screencap -p /sdcard/jump.png')
    os.system('adb pull /sdcard/jump.png')

def find_chess_x(im):
    flag = False
    for j in range(int(w*1/3), int(w*2/3)):
        for i in range(int(h*1/6), int(h*5/6)):
            pixel = im[j, i]
            if 55<pixel[0]<67 and 47<pixel[1]<59 and 45<pixel[2]<59:
                flag = True
                break
        if flag:
            break
    return i+3

def find_next_x(im):
    min_w = 0
    min_h = 0
    max_h = 0
    flag = False
    for j in range(int(w*1/3), int(w*2/3)):
        for i in range(int(h*1/6), int(h*5/6)):
            pixel = im[j, i]
            if 240<pixel[0] and 240<pixel[1] and 240<pixel[2]:
                min_w = j
                min_h = i
                flag = True
                break
        if flag:
            break
    for i in range(int(h*5/6), int(h*1/6), -1):
        pixel = im[min_w, i]
        if 240<pixel[0] and 240<pixel[1] and 240<pixel[2]:
            max_h = i
            break
    x = int((min_h+max_h)/2)
    return x

def jump(distance):
    press_time = int(distance * 1.59)
    x = int(random.uniform(490, 590))
    y = int(random.uniform(1570, 1590))
    cmd = 'adb shell input swipe {} {} {} {} {}'.format(*[x, y, x, y, press_time])
    os.system(cmd)

def main():
    distance = 453
    jump(distance)
    while True:
        time.sleep(0.8)
        get_screenshot()
        im = cv2.imread('jump.png')
        global w, h
        w, h, _ = im.shape
        chess_loc = find_chess_x(im)
        next_loc = find_next_x(im)
        print(chess_loc, next_loc)
        distance = abs(chess_loc - next_loc)
        jump(distance)

if __name__ == '__main__':
    main()
