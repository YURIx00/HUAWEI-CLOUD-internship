import pandas as pd  # 数据存储
import requests  # 网页内容获取
import re  # 解析数据
from lxml import etree  # 解析数据
import random
import time  # 反反爬
from fastprogress import master_bar, progress_bar  # 进度条显示

def sleep_milliseconds(milliseconds):
    seconds = milliseconds / 1000.0
    time.sleep(seconds)

def get_user_agent():
    """随机生成一个浏览器用户信息"""

    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7',
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
    ]

    agent = random.choice(user_agents)

    return {
        'User-Agent': agent
    }


def get(url):
    """
    获取网页源码
    url: 目标网页的地址
    return:网页源码
    """
    res = requests.get(url=url, headers=get_user_agent())
    return res.text


def get_url(res_text):
    """
    获取源码中每个二手房详情页的url
    res_text:网页源码
    return:列表形式的30个二手房详情页的url
    """
    re_f = '<a class="" href="(.*?)" target="_blank"'
    url_list = re.findall(re_f, res_text)
    return url_list


def get_else_data(res_text):
    res_text = etree.HTML(res_text)

    title = res_text.xpath("//div[@class='sellDetailHeader']//h1/@title")

    return dict(zip(['标题'], [title]))


def get_data(res_text):
    """获取房屋的详细数据"""
    res_text = etree.HTML(res_text)

    # 获取房屋的标题
    title = res_text.xpath("//div[@class='sellDetailHeader']//h1/@title")
    # 获取房屋的总价
    total_price = res_text.xpath("//div[@class='overview']//div/span/text()")[2]
    # 获取房屋的单价
    price = res_text.xpath("//div[@class='overview']//div/span/text()")[3]
    # 获取房屋的地段
    place = res_text.xpath("//div[@class='overview']//div/span/a/text()")

    ## 房屋基本信息获取
    # 获取房屋基本信息的标题
    lab = res_text.xpath("//div[@class='base']//span/text()")
    # 获取房屋基本信息的内容
    val = res_text.xpath("//div[@class='base']//li/text()")

    ## 获取房源交易信息
    # 获取房源交易标题
    key1 = res_text.xpath("//div[@class='transaction']//span[1]//text()")
    # 获取房源交易信息内容
    trans = res_text.xpath("//div[@class='transaction']//span[2]//text()")

    ## 获取房源特色信息
    # 获取房源特色标题
    key = res_text.xpath("//div[@class='baseattribute clear']/div[@class='name']/text()")
    # 获取房源特色内容
    val1 = res_text.xpath("//div[@class='baseattribute clear']/div[@class='content']/text()")

    # 返回包含上述信息的字典
    return dict(zip(['标题', '总价格', '单价', '地段'] + lab + key1 + key,
                    [title, total_price, price, place] + val + trans + val1))
    #return [title, total_price, price, place] + val + trans + val1


def main(qu, start_pg=1, end_pg=100, download_times=1):
    print('爬虫程序开始运行')
    """爬虫程序
    qu: 传入要爬取的qu的拼音的列表
    start_pg:开始的页码
    end_pg:结束的页码
    download_times:第几次下载
    """
    for q in qu:

        # 获取当前区的首页url
        url = 'https://bj.lianjia.com/ershoufang/' + q + '/'
        # url = 'https://bj.lianjia.com/ershoufang/'
        # 数据储存的列表
        data = []
        # 文件保存路径
        filename = '二手房-' + q + '第' + str(download_times) + '次下载.csv'

        print('二手房-' + q + '第' + str(download_times) + '次下载')
        mb = master_bar(range(start_pg, end_pg + 1))

        for i in mb:

            # 获取每页的url
            new_url = url + 'pg' + str(i) + '/'

            # 获取当前页面包含的30个房屋详情页的url
            url_list = get_url(get(new_url))

            for l in progress_bar(range(len(url_list)), parent=mb):

                # 反爬随机停止一段时间
                a = random.randint(2, 5)
                if l % a == 0:
                    sleep_milliseconds(2 * random.random())

                # 获取当前页面的源码
                text = get(url_list[l])
                # 获取当前页面的房屋信息
                data.append(get_data(text))

                # 反爬随机停止一段时间
                sleep_milliseconds(3 * random.random())  # random.random()随机生成0-1之间的小数
                mb.child.comment = '正在爬取第' + str(l + 1) + '条数据!!'
            mb.main_bar.comment = '正在爬取第' + str(i + 1) + '页数据!!'

            # 反爬随机停止一段时间
            sleep_milliseconds(5 * random.random())

            if i % 5 == 0:
                # 每5页保存一次数据
                pd.DataFrame(data).to_csv(filename, encoding='GB18030')
                mb.write('前' + str(i) + '页数据已保存')
        # 保存数据
        pd.DataFrame(data).to_csv(filename, encoding='GB18030')
        print('二手房-' + q + '第' + str(download_times) + '次下载完成')
main(['haidian'], 51, 60, 3)
