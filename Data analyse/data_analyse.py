from pyecharts import options as opts
from pyecharts.charts import Pie, WordCloud, Bar
import pandas as pd
import jieba.analyse
from collections import Counter


def extractTag(text):
    tagsList = []
    jieba.add_word("新型冠状病毒")
    jieba.add_word("新冠")
    jieba.add_word("无症状感染者")
    jieba.add_word("确诊病例")
    jieba.add_word("疑似病例")
    jieba.add_word("核酸检测")
    jieba.add_word("境外输入")
    jieba.add_word("2020")
    text_split_no = []
    f = open("stop_words.txt", "r")
    text_split_no = f.read().split(" ")
    if text:
        for i in text:
            tags = jieba.analyse.extract_tags(i, topK=40, withWeight=True)  # jieba分词一下
            for tag in tags:
                if tag[0] not in text_split_no:
                    tagsList.append(tag[0])
        print(tagsList)
    return tagsList


def wordcloud_base(result1, month) -> WordCloud:
    time = "./" + str(month) + "月词云.html"
    c = (

        WordCloud()
            .add("", result1, word_size_range=[20, 90], shape='star')
            .set_global_opts(title_opts=opts.TitleOpts(title="词云-基本示例"))
            .render(time)
    )
    return c


def pies(x, y, month):
    pie = (

        Pie()
            .add('热点词语词频', [(i, j) for i, j in zip(x, y)])
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    time = "./" + str(month) + "月Pie.html"
    pie.render(time)
    #pie.render('./测试Pie.html')


def pies_rose(x, y, month):
    pie = (
        Pie()
            .add(
            "",
            [(i, j) for i, j in zip(x, y)],
            radius=["30%", "75%"],
            center=["75%", "50%"],
            rosetype="area",
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-玫瑰图"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    time = "./" + str(month) + "月Pie_Rose.html"
    pie.render(time)
    #pie.render('./测试Pie_Rose.html')


def bars(x, y, month):
    bar = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("词频", y)
            .set_global_opts(title_opts=opts.TitleOpts(title="区域缩放柱状图"),
                             datazoom_opts=opts.DataZoomOpts(type_="slider"))
    )
    time = "./" + str(month) + "月Bar.html"
    bar.render(time)
    #bar.render('./测试Bar.html')


def init():
    filename = input()
    starbucks1 = pd.read_csv(filename).astype(str)
    friendsList = []
    print("输入数据月份：\n")
    month = input()
    for x in starbucks1.values:
        friendsList.append(x[3])
    extractTag(friendsList)
    result = Counter(extractTag(friendsList))
    result1 = result.most_common(500)  # 取500个
    lists = list(result1)
    x = []
    y = []
    for i in range(0, 25):
        temp = list(lists[i])
        x.append(temp[0])
        y.append(temp[1])
    print(x)
    print(y)
    wordcloud_base(result1, month)
    pies(x, y, month)
    pies_rose(x, y, month)
    bars(x, y, month)


init()
