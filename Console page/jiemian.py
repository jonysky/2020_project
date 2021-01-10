import time
import runpy
import tkinter
import tkinter.messagebox
import BlogSpider
from Web_spider import BlogSpider
from tkinter import Tk, LEFT
def m2():#查询成功子界面
 myWindow1 = Tk()
#设置标题
 myWindow1.title('微博爬取系统')
 myWindow1.geometry('600x500')
 myWindow1.resizable(width=True, height=True)
 ll1 = tkinter.Label(myWindow1, text='查询结果')
 ll1.place(x=50, y=10)
 t1 = tkinter.Text(myWindow1, height=5)
 t1.place(x=0,y=40)
 b2 = tkinter.Button(myWindow1, text='生成图表', width=0, height=0, command=None)
 b2.place(x=50, y=150)
 t2 = tkinter.Text(myWindow1, height=5)
 t2.place(x=0, y=200)
 myWindow1.mainloop()

myWindow = Tk()#开始界面
#设置标题
myWindow.title('微博爬取系统')
#设置窗口大小
myWindow.geometry('600x500')
myWindow.resizable(width=True, height=True)
l1 = tkinter.Label(myWindow, text='是否需要更新cookie')
l1.place(x=50,y=10)
r1 = tkinter.Radiobutton(myWindow, text='Y',value='A',command=None)
r1.place(x=250,y=10)
r2 = tkinter.Radiobutton(myWindow, text='N',value='B',command=None)
r2.place(x=350,y=10)
l2 = tkinter.Label(myWindow, text='请输入关键字')
l2.place(x=50,y=40)
var_name=tkinter.StringVar()
var_name.set('zyc')
e2 = tkinter.Entry(myWindow,textvariable=var_name,show=None)
e2.place(x=200,y=40)
l3 = tkinter.Label(myWindow, text='请输入起始日期')
l3.place(x=50,y=70)
var_start=tkinter.StringVar()
var_start.set('2020-11-11-11')
e3 = tkinter.Entry(myWindow,textvariable=var_start, show=None)
e3.place(x=200,y=70)
l4 = tkinter.Label(myWindow, text='请输入终止日期')
l4.place(x=50,y=100)
var_end=tkinter.StringVar()
var_end.set('2020-11-11-12')
e4 = tkinter.Entry(myWindow, textvariable=var_end,show=None)
e4.place(x=200,y=100)

def x():
 name=var_name.get()
 start=var_start.get()
 end=var_end.get()
 if name=='zyc'and start=='2020-11-11-11'and end=='2020-11-11-12':#判断关键字日期格式是否正确
  tkinter.messagebox.showinfo(title='微博爬取系统', message='查询成功')
  myWindow.destroy()
  m2()
 else:
  tkinter.messagebox.showinfo(title='微博爬取系统', message='查询失败,重新输入')
  myWindow.update()
b1 = tkinter.Button(myWindow, text='查询', width=0, height=0, command=x)
b1.place(x=400,y=100)
myWindow.mainloop()
