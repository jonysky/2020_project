# 2020_project
开源大作业：宋金沛，穆晓彬，张恒天，侯照亮，桑楠

项目说明:

Spider：

.idea和venv是pycharm新建项目生成的文件，可以不用管

process包：

	_pycache_也是pycharm自己生成的。

	process.py：一些处理函数，相应的功能有注释。

Web_spider包：

	_pycache_是pycharm自己生成的。

	cookie_file：爬取所需的cookies

	BlogSpider.py：爬取数据的主代码。

	hour_fenge.py：用于分割时间的函数

data analyse:

        stop_words.py：是用于生成数字停止词的文件，输出stop_words.txt
	
	data_analyse.py:是用读取.csv文件并进行数据处理与数据可视化的过程（分两次输入读取文件名与数据对应月份），输出.html文件
	
	x月词云（Pie/Pie_Rose/Bar）图.html:分别为将数据可视化后的文件

Console page:

jiemian.py : 控制台页面的展示
