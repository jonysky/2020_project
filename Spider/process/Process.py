import datetime
import time
from selenium import webdriver
import re


'''获取文件中存储的cookie'''

def read_cookie():
    with open('cookie_file', 'r', encoding='utf-8') as f:  # 打开文件
        line = f.readline()  # 读取所有行
    f.close()
    return line


'''更新文件中存储的cookie'''

def write_cookie():
    temp = 'y'#input("更新在Chrome登录http://www.weibo.cn时所获取的cookie（输入n/N不更新cookie）:")
    if (temp == 'n' or temp == 'N'):
        return
    cookie = temp
    with open('cookie_file', 'w', encoding='utf-8') as f:  # 打开文件
        f.write(cookie)
    f.close()
    return cookie



''' 获取全文微博处理函数：展开需要获取全文的微博并提取'''


def geturl(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    #注释不显示Chrome打开爬取过程，注释可以不显示
    #browser = webdriver.Chrome()
    browser.get(url)
    try:
        #此处需要填微博账号的用户名和密码，不然登不上
        browser.find_element_by_css_selector("#loginname").send_keys(
            "17866553634")
        browser.find_element_by_css_selector(".info_list.password input[node-type='password']").send_keys(
            "qwe123.")
        browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()
    except:
        print("no login")
        try:
            t = browser.find_element_by_xpath(".//div[@class='WB_text W_f14']").text.replace('\n','').replace(' ','').replace('\r','').strip()
        except:
            t = None
            print("no data")
        browser.close()
        return t
    browser.get(url)
    time.sleep(1)
    try:
        t = browser.find_element_by_xpath(".//div[@class='WB_text W_f14']").text.replace('\n','').replace(' ','').replace('\r','').strip()
    except:
        t = None
        print("no data")
    browser.close()
    return t



''' 微博创建日期处理函数 '''

def time_process(time):
    time = str(time)
    if '月' in time:
        if '年' not in time:
            dangqian_year = datetime.datetime.now().strftime('%Y')
            time = dangqian_year + '-' + time
        time = time.replace(r'年', '-').replace(r'月', '-').replace(r'日', '')
    if time.startswith('今天'):
        dangqian_date = datetime.datetime.now().strftime('%Y-%m-%d')
        time = time.replace(r'今天', dangqian_date + ' ')
    if time.endswith('分钟前'):
        dangqian_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        time = dangqian_time
    return time


''' 转发、评论数处理函数 '''

def num_process(char_num):
    if (len(char_num) <= 4):
        return '0'
    else:
        return str(char_num.split()[1])


'''去除emoji表情'''

def filter_emoji(desstr, restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)