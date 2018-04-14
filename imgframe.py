# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import os
from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from PIL import Image
import matplotlib.pyplot as plt # plt 用于显示图片
import numpy as np


colorrgb = []
filelists = []
path = []

def close():
    exit(0)

def scan_files(file):           #扫描文件夹中所有文件并返回一个列表
    for root,dirs,files in os.walk(file):
        global filelists,path
        filelists = files
        path = root
    return filelists,path

def openfile():
    filedir = filedialog.askdirectory()  # 打开文件夹
    filelists = scan_files(filedir)  # 得到文件夹中的所有文件



def choosecolor():      #得到用户需要用的颜色R,G,B
    color = colorchooser.askcolor()
    global colorrgb
    colorrgb = color[0]
    return colorrgb


def start():
    r = colorrgb[0]
    g = colorrgb[1]
    b = colorrgb[2]
    n = len(filelists)
    width = 1
    yuzhi = 0
    for each in range(n):
        fileimg = path + "/" + filelists[each]        #得到图片的完整路径
        img = Image.open(fileimg)  # 只是读取图片
        imgarr = np.array(img)  # 将图片转化为数组，此时是三维的[:,:,3]

        img2 = img.convert("L")  # 将图片转化为灰度图

        img2arr = np.array(img2)  # 将灰度图转化为数组，此时是一维

        threshlod = 25  # 设置域值进行二值化
        table = np.zeros((400, 400))
        for x in range(400):
            for y in range(400):
                if img2arr[x, y] < threshlod:
                    table[x, y] = 0
                else:
                    table[x, y] = 1

        # 以下4个for循环用来 找出x1,y1,x2,y2
        for x in range(400):
            i = 0
            for y in range(400):
                if table[x, y] == 1:
                    i += 1
                    if i == 5:
                        x2 = x + yuzhi
                        break

        for y in range(400):
            i = 0
            for x in range(400):
                if table[x, y] == 1:
                    i += 1
                    if i == 5:
                        y2 = y + yuzhi
                        break

        for x in range(399, -1, -1):
            i = 0
            for y in range(400):
                if table[x, y] == 1:
                    i += 1
                    if i == 5:
                        x1 = x - yuzhi
                        break

        for y in range(399, -1, -1):
            i = 0
            for x in range(400):
                if table[x, y] == 1:
                    i += 1
                    if i == 5:
                        y1 = y - yuzhi
                        break

        #以下代码将图片进行框选
        for x in range(400):
            for y in range(400):
                if x >= x1 - width and x <= x1 + width and y >= y1 and y <= y2:
                    imgarr[x, y, 0] = r
                    imgarr[x, y, 1] = g
                    imgarr[x, y, 2] = b
                elif x >= x2 - width and x <= x2 + width and y >= y1 and y <= y2:
                    imgarr[x, y, 0] = r
                    imgarr[x, y, 1] = g
                    imgarr[x, y, 2] = b
                elif y >= y1 - width and y <= y1 + width and x >= x1 and x <= x2:
                    imgarr[x, y, 0] = r
                    imgarr[x, y, 1] = g
                    imgarr[x, y, 2] = b
                elif y >= y2 - width and y <= y2 + width and x >= x1 and x <= x2:
                    imgarr[x, y, 0] = r
                    imgarr[x, y, 1] = g
                    imgarr[x, y, 2] = b

        #以下代码用来保存框选之后的图片
        plt.imshow(imgarr)
        plt.axis('off')
        plt.savefig(fileimg)

        if(each == n-1):
            print("It's over!")

def goin():

    root.destroy()
    secondwindow = Tk()

    text = Text(secondwindow, width=50, height=20).grid(rowspan=5, columnspan=2, padx=5, pady=10)
    startbutton = Button(secondwindow, text="开始框选", command=start).grid(row=2, column=2, padx=25, pady=15)
    closebutton = Button(secondwindow, text="  退   出  ", command=close).grid(row=3, column=2, padx=25, pady=15)


    mainloop()


root= Tk()
root.title("自动框选蚕茧")

openbutton = Button(root,text="选择文件",command = openfile).grid(row = 0,column = 0,padx =25,pady = 15)
colorbutton = Button(root, text="选择颜色", command=choosecolor).grid(row=1, column=0,padx =25,pady = 15)
colorbutton = Button(root, text="确定", command=goin).grid(row=2, column=0,padx =25,pady = 15)

mainloop()