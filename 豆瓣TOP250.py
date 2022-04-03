# -*- coding = utf-8 -*-
# @Time : 2022/3/31 20:18
# @Author : B20040710-崔冰
# @file : 豆瓣TOP250.py
# @software : PyCharm


from bs4 import BeautifulSoup  # 网页解析获取数据
import re  # 正则表达式进行文字匹配
# import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行Excel操作
import urllib.request


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影Top250.xls"
    # 3.保存数据
    saveData(datalist, savepath)
    # askURL("https://movie.douban.com/top250?start=0")


findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findName = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 1.爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)  # 测试查看电影item
            data = []  # 保存一部电影所有信息
            item = str(item)  # 类型转换
            # 获取影片链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            names = re.findall(findName, item)
            if len(names) == 2:
                cname = names[0]  # 添加中文名
                data.append(cname)
                oname = names[1].replace("/", "")  # 去掉无关的符号
                data.append(oname)
            else:
                data.append(names[0])
                data.append('   ')  # 外国名字留空
            rating = re.findall(findRating, item)[0]
            data.append(rating)
            judge = re.findall(findJudge, item)[0]
            data.append(judge)
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")  # 去掉句号
                data.append(inq)  # 添加概述
            else:
                data.append("")  # 留空
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉<br/>
            data.append(bd.strip())  # 去掉前后的空格
            datalist.append(data)  # 把处理好的一部电影信息存入datalist
    # print(datalist)
    # print(link)
    return datalist


# 得到一个指定的URL的网页内容
def askURL(url):  # 模拟浏览器头部信息，向浏览器发送消息
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55"}
    # 用户代理，告诉服务器我们是什么类型的机器，浏览器（本质上是告诉浏览器我们可以接受什么水平的文件内容）
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e)
        if hasattr(e, "reason"):
            print(e)
    return html


# 3.保存数据
def saveData(datalist, savepath):
    # print("save...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影top250', cell_overwrite_ok=True)  # 创建工作表
    # sheet.write(0, 0, "hello")
    col = ("电影链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, 250):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)  # 保存


if __name__ == '__main__':  # 当程序被执行时
    main()  # 调用程序
    print("爬取完毕！")
