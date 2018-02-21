#coding=utf-8
from pyutils import *
from Tkinter import *
import tkinter
from tkinter.filedialog import askdirectory
import tkMessageBox
import urllib
import json
import mp3play
import time
import pygame
import shutil
import subprocess
list_music = []

#定义点击按钮响应的函数
def music():
    
    #print "按钮点击"
    #先判断用户是否在编辑框输入了内容
    if E.get() == '':
        #发出警告，需要先import tkMessageBox
        tkMessageBox.showinfo("提示：","请先输入内容！")
        #使用return，当满足前面的条件时，不在往下执行
        return
    #使用网易api，发送请求，需要import urllib
    #报错，需要将汉字编码程ascii，才能添加到链接中
    name = E.get().encode('utf-8')
    name = urllib.quote(name)
    userNickName = '*****'
    html = urllib.urlopen('https://www.chnhuangbo.cn/?userNickName=%s&keywords=%s'%(userNickName, name)).read()
    #返回json格式数据,可用正则匹配需要数据，也可使用json.loads()
    # print html
    #将返回文件转化为json格式，提取所需要的数据，需要import json
    list_songs = json.loads(html)
    LB.delete(0,END)
    for i in range(len(list_songs)):
        #注意insert参数
        LB.insert(i,list_songs[i]['singer']+"-"+list_songs[i]['name'])
        #先获取到歌曲url列表
        list_music.append(list_songs[i]['musicUrl'])
#定义双击列表响应函数

def download(event):
    #获取点击后返回的结果curselection()
    urlnum = LB.curselection()[0]
    # print(urlnum)
    #不用流媒体播放，先下载下来再播放
    songname = LB.get(urlnum)
    pathsong = str(pathEntry.get()) + songname + '.mp3'
    # print(pathsong)
    if os.path.isfile(pathsong):
        tkMessageBox.showinfo('温馨提示', songname + '\n在该目录已存在')
    else:
        urllib.urlretrieve(list_music[urlnum], pathsong)
        tkMessageBox.showinfo('温馨提示', songname + '\n已成功下载')

# def click(event):
#     #获取点击后返回的结果curselection()
#     print(LB.curselection())
#     urlnum = LB.curselection()[0]
#     py_print(urlnum)
#     #不用流媒体播放，先下载下来再播放
#     songname = LB.get(urlnum)
#     py_print(songname)
#     py_print(list_music[urlnum])
#     # mp3 = mp3play.load(list_music[urlnum])
#     # mp3.play()
#     pygame.mixer.init()
#     pygame.mixer.music.load(list_music[urlnum])
#     pygame.mixer.music.play()
#     time.sleep(100)
    

def selectPath():
    path_ = askdirectory()
    global path
    path.set(path_ + '/')
    if path == '/':
        path.set('')
    # print(path)

def createTK():
    #创建父窗口对象，
    top = Tk()
    path = StringVar()
    index_row = 0
    #可以设置窗口的属性,如：标题，大小
    top.title(u"音乐下载器——Ripple")
    top.geometry('400x350+800+300')
    #创建编辑框，放到父窗口top上,用pack显示
    label = Label(top,text = "All you want are here")
    label.grid(row=index_row, column=1)
    index_row += 1
    #定义标签
    label = Label(top,text = "----------------",fg = 'black')
    label.grid(row=index_row, column=0)
    label = Label(top,text = "----------------",fg = 'black')
    label.grid(row=index_row, column=1)
    label = Label(top,text = "----------------",fg = 'black')
    label.grid(row=index_row, column=2)
    index_row += 1

    label = Label(top,text = "Tips:双击下载")
    label.grid(row=index_row, column=2)
    index_row += 1


    label = Label(top,text = "关键词")
    label.grid(row=index_row, column=0)
    E = Entry(top)
    E.grid(row=index_row, column=1)
    #创建按钮,定义按钮触发的函数command
    B = Button(top,text="搜 索",width = '10', command = music)
    B.grid(row=index_row, column=2)
    #定义列表的响应函数
    index_row += 1

    scrollbar = Scrollbar(top)
    # scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.grid(row=index_row, column=4, sticky='ns')
    LB = Listbox(top,width = '50', yscrollcommand=scrollbar.set, listvariable = StringVar())
    scrollbar.configure(command=LB.yview)
    #绑定触发事件的方式-双击左键，和响应函数
    LB.bind('<Double-Button-1>',download)
    # LB.bind('<ButtonRelease-1>',click)
    LB.grid(row=index_row, columnspan=3)
    index_row += 1

    #定义标签
    label = Label(top,text = "----------------",fg = 'black')
    label.grid(row=index_row, column=0)
    label = Label(top,text = "----------------",fg = 'black')
    label.grid(row=index_row, column=1)
    label = Label(top,text = "----------------",fg = 'black')
    label.grid(row=index_row, column=2)
    index_row += 1

    label2 = Label(top,text = "目标路径:")
    label2.grid(row=index_row, column=0)
    pathEntry = Entry(top, textvariable = path)
    pathEntry.grid(row=index_row, column=1)
    selectBtn = Button(top, text = "路径选择", command = selectPath)
    selectBtn.grid(row=index_row, column=2)

    #循环向windows发送消息，用于显示窗口
    top.mainloop()


if __name__ == '__main__':
    createTK()