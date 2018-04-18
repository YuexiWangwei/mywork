# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
import os
from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from tkinter.scrolledtext import ScrolledText
from PIL import Image
import shutil
# import matplotlib.pyplot as plt # plt 用于显示图片,调试使用！
import numpy as np
#import scipy.misc
import xlwt


colorrgb = []
filelists = []
path = []

xml = '''<annotation verified="no">
  <folder>JPEGImages</folder>
  <filename>%s</filename>
  <path>%s</path>
  <source>
    <database>Unknown</database>
  </source>
  <size>
    <width>%d</width>
    <height>%d</height>
    <depth>3</depth>
  </size>
  <segmented>0</segmented>
  <object>
    <name>%s</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <Difficult>0</Difficult>
    <bndbox>
      <xmin>%d</xmin>
      <ymin>%d</ymin>
      <xmax>%d</xmax>
      <ymax>%d</ymax>
    </bndbox>
  </object>
</annotation>'''


def close():
    exit(0)

def scan_files(file):           #扫描文件夹中所有文件并返回一个列表
    for root,dirs,files in os.walk(file):
        global filelists,path
        filelists = files
        path = root
        path = path + "/"
    return filelists,path

def openfile():
    filedir = filedialog.askdirectory()  # 打开文件夹
    filelists = scan_files(filedir)  # 得到文件夹中的所有文件

    #显示当前文件夹路径
    labelfile.delete(1.0,END)
    labelfile.insert(INSERT,path)

def choosecolor():      #得到用户需要用的颜色R,G,B
    color = colorchooser.askcolor()
    global colorrgb
    colorrgb = color[0]

    #显示当前颜色的RGB值
    colors = "  R:"+str(int(colorrgb[0]))+"   G:"+str(int( colorrgb[1]))+"    B:"+str(int(colorrgb[2]))
    labelcolor.delete(1.0,END)
    labelcolor.insert(INSERT,colors)
    return colorrgb

def goin():

    root.destroy()
    secondwindow = Tk()
    secondwindow.title("自动框选蚕茧")
    labelinput = Label(secondwindow, text="输入开始序号：", font="幼圆")
    intnumber = IntVar
    numberentry = Entry(secondwindow, width=18, textvariable=intnumber)

    def start():
        r = colorrgb[0]
        g = colorrgb[1]
        b = colorrgb[2]
        n = len(filelists)
        width = 1
        yuzhi = 0

        # 改变到当前工作目录并创建jpg和xml文件夹
        os.chdir(path)
        os.mkdir("jpg")
        os.mkdir("xml")

        #创建一个前后图片名字对应的excel文件
        relatedexcel = xlwt.Workbook(encoding='utf-8')
        sheet1 = relatedexcel.add_sheet('Sheet1')
        sheet1.write(0, 0, "图片原名称")
        sheet1.write(0, 1, "修改后名称")

        #定义文件的序号
        number = int(numberentry.get())
        print(number)

        for each in range(n):
            fileimg = path + filelists[each]  # 得到图片的完整路径

            img = Image.open(fileimg)  # 只是读取图片
            imgarr = np.array(img)  # 将图片转化为数组，此时是三维的[:,:,3]

            #得到图片的长宽数值
            X = imgarr.shape[1]
            Y = imgarr.shape[0]

            img2 = img.convert("L")  # 将图片转化为灰度图

            img2arr = np.array(img2)  # 将灰度图转化为数组，此时是一维

            threshlod = 20  # 设置域值进行二值化
            table = np.zeros((Y, X))

            for x in range(Y):
                for y in range(X):
                    if img2arr[x, y] < threshlod:
                        table[x, y] = 0
                    else:
                        table[x, y] = 1

            # 以下4个for循环用来 找出x1,y1,x2,y2
            for x in range(Y):
                i = 0
                for y in range(X):
                    if table[x, y] == 1:
                        i += 1
                        if i == 5:
                            x2 = x + yuzhi
                            break

            for y in range(X):
                i = 0
                for x in range(Y):
                    if table[x, y] == 1:
                        i += 1
                        if i == 5:
                            y2 = y + yuzhi
                            break

            for x in range(Y-1, -1, -1):
                i = 0
                for y in range(X):
                    if table[x, y] == 1:
                        i += 1
                        if i == 5:
                            x1 = x - yuzhi
                            break

            for y in range(X-1, -1, -1):
                i = 0
                for x in range(Y):
                    if table[x, y] == 1:
                        i += 1
                        if i == 5:
                            y1 = y - yuzhi
                            break
            #
            # # 以下代码将图片进行框选
            # for x in range(Y):
            #     for y in range(X):
            #         if x >= x1 - width and x <= x1 + width and y >= y1 and y <= y2:
            #             imgarr[x, y, 0] = r
            #             imgarr[x, y, 1] = g
            #             imgarr[x, y, 2] = b
            #         elif x >= x2 - width and x <= x2 + width and y >= y1 and y <= y2:
            #             imgarr[x, y, 0] = r
            #             imgarr[x, y, 1] = g
            #             imgarr[x, y, 2] = b
            #         elif y >= y1 - width and y <= y1 + width and x >= x1 and x <= x2:
            #             imgarr[x, y, 0] = r
            #             imgarr[x, y, 1] = g
            #             imgarr[x, y, 2] = b
            #         elif y >= y2 - width and y <= y2 + width and x >= x1 and x <= x2:
            #             imgarr[x, y, 0] = r
            #             imgarr[x, y, 1] = g
            #             imgarr[x, y, 2] = b

            #找到蚕茧的种类,生成标签时插入
            kinds = []
            if (filelists[each].find("bie")) != -1:
                kinds = "bie"
            elif (filelists[each].find("hege")) != -1:
                kinds = "hege"
            elif (filelists[each].find("huang")) != -1:
                kinds = "huang"
            elif (filelists[each].find("ji")) != -1:
                kinds = "ji"
            elif (filelists[each].find("shuang")) != -1:
                kinds = "shuang"

            #将需要保存的xml文件的名称提取出来
            # filename = filelists[each].split(sep = ".p")
            # xmlname = filename[0] + ".xml"

            #用数字的方式保存的图片名称与xml文件名称
            tempname = "%06d"%(number)
            number += 1
            xmlname =tempname + ".xml"
            filename =tempname + ".jpg"

            try:
                # 以新名字保存图片
                # plt.imshow(imgarr)
                # plt.axis('off')
                # plt.savefig(filename)
                os.chdir(path)
                shutil.copy(filelists[each],path+"jpg")
                os.chdir(path + "jpg")
                os.rename(filelists[each],filename)
                #scipy.misc.imsave(filename,img)

                # 以新图片名字保存相应xml文件
                os.chdir(path + "xml")
                with open(xmlname,'w') as f:
                    f.write(xml%(fileimg,path,X,Y,kinds,x1,y1,x2,y2))

                #生成图片前后对应名字的excel表格
                sheet1.write(each+1,0,filelists[each])
                sheet1.write(each+1,1,filename)


                states = filelists[each] + "框选成功\n"

            except:
                states = filelists[each] + "框选错误\n"

            #实时显示每张图片框选状态
            textshow.insert(INSERT,states)
            textshow.see(END)
            textshow.update()

            if (each == n-1):
                textshow.insert(INSERT, "所有图片框选完成！")
                textshow.see(END)
                textshow.update()

        #保存excel表格
        os.chdir(path)
        relatedexcel.save("relatedexcel.xls")

    textshow = ScrolledText(secondwindow, width=50, height=20, font="幼圆")
    startbutton = Button(secondwindow, text="开始框选", command=start, font="幼圆")
    closebutton = Button(secondwindow, text=" 退   出 ", command=close, font="幼圆")

    textshow.grid(rowspan=5, columnspan=2, padx=5, pady=10)
    labelinput.grid(row = 1,column = 2,padx = 25,pady = 5)
    numberentry.grid(row=2, column=2, padx=25, pady=1)
    startbutton.grid(row=3, column=2, padx=25, pady=15)
    closebutton.grid(row=4, column=2, padx=25, pady=15)

    mainloop()

root= Tk()
root.title("自动框选蚕茧")

openbutton = Button(root,text="选择文件",command = openfile, font="幼圆")
colorbutton = Button(root, text="选择颜色", command=choosecolor, font="幼圆")
labelfile = Text(root,width = 40,height = 1,font = "幼圆")
labelcolor = Text(root,width = 40,height = 1,font = "幼圆")
surebutton = Button(root, text=" 确   定 ", command=goin, font="幼圆")

openbutton.grid(row = 0,column = 0,padx =15,pady = 15)
colorbutton.grid(row=1, column=0,padx =15,pady = 15)
labelfile.grid(row = 0,column = 1,padx = 15,pady = 15)
labelcolor.grid(row = 1,column = 1,padx = 15,pady = 15)
surebutton.grid(row=2, columnspan =2,padx =25,pady = 15)

mainloop()