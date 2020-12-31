import csv
from process import Process
from tkinter import Tk, LEFT
import tkinter
import tkinter.messagebox
import datetime
import re
import time
import requests
from bs4 import BeautifulSoup
from Web_spider.hour_fenge import hour_fenge
from process.Process import geturl, time_process, num_process, filter_emoji

# 要访问的微博搜索接口URL
url_template = 'https://s.weibo.com/weibo?q={}&scope=ori&suball=1&timescope=custom:{}:{}&Refer=g&page={}'



"""抓取关键词某一页的数据"""

def fetch_weibo_data(keyword, start_time, end_time, page_id,cookie):
    #headers是Chrome自己的headers
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    cookies = {
        'Cookie':cookie
    }
    resp = requests.get(url_template.format(keyword, start_time, end_time, page_id),headers = headers,cookies = cookies)
    print(url_template.format(keyword,start_time,end_time,page_id))
    soup = BeautifulSoup(resp.text, 'lxml')
    all_contents = soup.select('.card-wrap')

    wb_count = 0
    mblog = []  # 保存处理过的微博
    for card in all_contents:
        if (card.get('mid') != None):# 如果微博ID不为空则开始抓取
            #测试发现，很多带V的用户回很大程度上拖慢速度，所以视情况而定吧
            if (card.find('i', attrs={'class': 'icon-vip icon-vip-b'}) or card.find('i', attrs={'class': 'icon-vip icon-vip-y'}) is None
            or card.find('i', attrs={'class': 'icon-vip icon-vip-r'}) or card.find('i', attrs={'class': 'icon-vip icon-vip-g'}) is None):
            # if(card.find('i',attrs = {'class':'icon-vip icon-vip-b'}) is None and card.find('i',attrs = {'class':'icon-vip icon-vip-y'}) is None
            # and card.find('i',attrs = {'class':'icon-vip icon-vip-r'}) is None and card.find('i',attrs = {'class':'icon-vip icon-vip-g'}) is None):
                wb_username = card.select_one('.txt').get('nick-name')  # 微博用户名
                href = card.select_one('.from').select_one('a').get('href')
                re_href = re.compile('.*com/(.*)/.*')
                wb_userid = re_href.findall(href)[0]  # 微博用户ID
                s = card.select_one('.txt').select_one('a[action-type="fl_unfold"]')
                if (s is None):
                    wb_content = card.select_one('.txt').text.replace('\n', '').replace(' ', '').replace('\r','').strip()  # 微博内容
                else:
                    #获取展开全文后的微博
                    url = 'https:' + card.select_one('.txt').find('a', {'action-type': 'fl_unfold'}).get('href')
                    print(url)
                    temp = geturl(url)
                    if temp is not None:
                        wb_content = temp
                    else:
                        continue
                wb_create = card.select_one('.from').select_one('a').text.strip()  # 微博创建时间
                wb_url = 'https:' + str(card.select_one('.from').select_one('a').get('href'))  # 微博来源URL
                wb_id = str(card.select_one('.from').select_one('a').get('href')).split('/')[-1].split('?')[0]  # 微博ID
                wb_createtime = time_process(wb_create)
                wb_forward = str(card.select_one('.card-act').select('li')[1].text)  # 微博转发数
                wb_forwardnum = num_process(wb_forward)
                wb_comment = str(card.select_one('.card-act').select('li')[2].text)  # 微博评论数
                wb_commentnum = num_process(wb_comment)
                wb_like = str(card.select_one('.card-act').select_one('em').text)  # 微博点赞数

                if (wb_like == ''):  # 点赞数的处理
                    wb_likenum = '0'
                else:
                    wb_likenum = wb_like

                blog = {'wb_id': wb_id,  # 微博id
                        'wb_username': wb_username,
                        'wb_userid': wb_userid,
                        'wb_content': wb_content,
                        'wb_createtime': wb_createtime,
                        'wb_forwardnum': wb_forwardnum,
                        'wb_commentnum': wb_commentnum,
                        'wb_likenum': wb_likenum,
                        'wb_url': wb_url
                        }
                mblog.append(blog)
                wb_count = wb_count + 1  # 表示此页的微博数

    print("--------- 正在爬取第%s页 --------- " % page_id + "当前页微博数：" + str(wb_count))
    return mblog




"""抓取关键词多页的数据"""


def fetch_pages(keyword, start_time, end_time,cookie):
    cookies = {
        "Cookie": cookie}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    resp = requests.get(url_template.format(keyword, start_time, end_time, '1'),cookies=cookies,headers = headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    t2 = soup.select_one('.card-wrap').select_one('p').text
    if (str(soup.select_one('.card-wrap').select_one('p').text).startswith('抱歉')):
        print("此次搜索条件无相关搜索结果！\n请重新选择条件筛选...")
        return
    else:
        mblogs = []  # 此次时间单位内的搜索全部结果先临时用列表保存，后存入csv
        try:
            # 每个时间段爬取前20页微博
            t = soup.select_one(".s-scroll").select("li")
            page_num = len(t)
            if (page_num>20):
                page_num = 20
        except:
            page_num = 1
        for page_id in range(page_num):
            page_id = page_id + 1
            try:
                mblogs.extend(
                    fetch_weibo_data(keyword, start_time, end_time, page_id, cookie))  # 每页调用fetch_data函数进行微博信息的抓取
                time.sleep(1)
            except Exception as e:
                print(e)
        # 写入csv
    with open(keyword+'.csv', 'a+', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        i = 0
        for i in range(len(mblogs)):
            row = [mblogs[i]['wb_id'], mblogs[i]['wb_username'], mblogs[i]['wb_userid'],
                   filter_emoji(mblogs[i]['wb_content']),
                   mblogs[i]['wb_createtime'], mblogs[i]['wb_forwardnum'], mblogs[i]['wb_commentnum'],
                   mblogs[i]['wb_likenum'],
                   mblogs[i]['wb_url']]
            writer.writerow(row)





if __name__ == '__main__':
    myWindow = Tk()  # 开始界面
    # 设置标题
    myWindow.title('微博爬取系统')
    # 设置窗口大小
    myWindow.geometry('600x500')
    myWindow.resizable(width=True, height=True)
    l1 = tkinter.Label(myWindow, text='是否需要更新cookie')
    l1.place(x=50, y=10)
    r1 = tkinter.Radiobutton(myWindow, text='Y', value='A', command=None)
    r1.place(x=250, y=10)
    r2 = tkinter.Radiobutton(myWindow, text='N', value='B', command=None)
    r2.place(x=350, y=10)
    l2 = tkinter.Label(myWindow, text='请输入关键字')
    l2.place(x=50, y=40)
    var_name = tkinter.StringVar()
    e2 = tkinter.Entry(myWindow, textvariable=var_name, show=None)
    e2.place(x=200, y=40)
    l3 = tkinter.Label(myWindow, text='请输入起始日期')
    l3.place(x=50, y=70)
    var_start = tkinter.StringVar()
    e3 = tkinter.Entry(myWindow, textvariable=var_start, show=None)
    e3.place(x=200, y=70)
    l4 = tkinter.Label(myWindow, text='请输入终止日期')
    l4.place(x=50, y=100)
    var_end = tkinter.StringVar()
    e4 = tkinter.Entry(myWindow, textvariable=var_end, show=None)
    e4.place(x=200, y=100)
    def x():
        Process.write_cookie()
        cookie = Process.read_cookie()

        keyword = var_name.get()
        start_time = var_start.get()
        end_time = var_end.get()
        time_start_jishi = time.time()  # 开始爬的系统时间
        # 对爬取时间段进行划分
        hour_all = hour_fenge(start_time, end_time)
        i = 0
        while i < len(hour_all):
            fetch_pages(keyword, hour_all[i][0], hour_all[i][1], cookie)
            print(hour_all[i][0] + ' 到 ' + hour_all[i][1] + ' 时间单位内的数据爬取完成！\n')
            i = i + 1
        time_end_jishi = time.time()  # 爬取结束后的系统时间

        print('数据全部爬取成功，用时:', (time_end_jishi - time_start_jishi))
    myWindow.destroy()

    b1 = tkinter.Button(myWindow, text='查询', width=0, height=0, command=x)
    b1.place(x=400, y=100)
    myWindow.mainloop()
    #建议在爬取数据前首先对网站的cookie进行更新。
    # Process.write_cookie()
    # cookie = Process.read_cookie()
    #
    # keyword = var_name.get()
    # start_time = var_start.get()
    # end_time = var_end.get()
    # time_start_jishi = time.time() #开始爬的系统时间
    # #对爬取时间段进行划分
    # hour_all = hour_fenge(start_time, end_time)
    # i = 0
    # while i < len(hour_all):
    #     fetch_pages(keyword, hour_all[i][0], hour_all[i][1],cookie)
    #     print(hour_all[i][0] + ' 到 ' + hour_all[i][1] + ' 时间单位内的数据爬取完成！\n')
    #     i = i + 1
    # time_end_jishi = time.time() #爬取结束后的系统时间
    #
    # print('数据全部爬取成功，用时:', (time_end_jishi - time_start_jishi))
