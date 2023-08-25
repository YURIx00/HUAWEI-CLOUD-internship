import pandas as pd  # 数据存储
import requests  # 网页内容获取
import re  # 解析数据
from lxml import etree  # 解析数据
import random
import time  # 反反爬
from bs4 import BeautifulSoup


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


def get_html(url):
    """
    获取网页源码
    url: 目标网页的地址
    return:网页源码
    """
    res = requests.get(url=url, headers=get_user_agent())
    return res.text


def get_url_by_html(res_html):
    """
    获取源码中每个二手房详情页的url
    res_html:网页源码
    return:列表形式的30个二手房详情页的url
    """
    re_f = '<a class="" href="(.*?)" target="_blank"'
    url_list = re.findall(re_f, res_html)
    return url_list


def parse_html(res_html):
    """获取房屋的详细数据"""
    soup = BeautifulSoup(res_html, 'html.parser')

    # 获取房屋的标题
    title = soup.select_one("div.sellDetailHeader h1")['title']

    # 获取房屋的总价
    # total_price = soup.select("div.overview div span")[2].get_text()
    total_price = soup.findAll("span", attrs={'class': 'total'})[0].get_text()

    # 获取房屋的单价
    price = soup.find("span", attrs={'class': 'unitPriceValue'}).get_text()[0:-4]

    # 获取房屋的地段
    place = [a.get_text() for a in soup.select("div.areaName span a")]

    place = list(filter(None, place))
    # 获取房屋基本信息
    ## 获取房屋基本信息的标题
    lab = [span.get_text() for span in soup.select("div.base span")]
    ## 获取房屋基本信息的内容
    val = [li.contents[-1].strip() for li in soup.select("div.base li")]

    # 获取房源交易信息
    ## 获取房源交易标题
    key1 = [span.get_text().strip() for span in soup.select("div.transaction span:nth-of-type(1)")]  # 获取第一个span标签的内容
    ## 获取房源交易信息内容
    trans = [span.get_text().strip() for span in soup.select("div.transaction span:nth-of-type(2)")]

    # 获取房源特色信息
    ## 获取房源特色标题
    key = [div.get_text().strip() for div in soup.select("div.baseattribute div.name")]
    ## 获取房源特色内容
    val1 = [div.get_text().strip() for div in soup.select("div.baseattribute div.content")]

    # 返回包含上述信息的字典
    return dict(zip(['标题', '总价格', '单价', '地段'] + lab + key1 + key,
                    [title, total_price, price, place] + val + trans + val1))


# lab:  ['房屋户型', '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况', '梯户比例', '供暖方式', '配备电梯']
# key1:  ['挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限', '产权所属', '抵押信息', '房本备件']
# key:  ['核心卖点', '小区介绍', '周边配套', '交通出行']

def myspider(qu, start_pg=1, end_pg=100, download_times=1):
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
        # 数据储存的列表
        data = []
        # 文件保存路径
        # filename_csv = 'SecondHand-' + q + str(download_times) + 'tims_download.csv'
        filename_excel = 'SecondHand_House_{}_{}_times_download.xlsx'.format(q, download_times)

        print(filename_excel)

        for i in range(start_pg, end_pg + 1):

            # 获取每页的url
            new_url = url + 'pg' + str(i) + '/'

            # 获取当前页面包含的30个房屋详情页的url
            url_list = get_url_by_html(get_html(new_url))

            for l in range(len(url_list)):

                # 反爬随机停止一段时间
                a = random.randint(2, 5)
                if l % a == 0:
                    sleep_milliseconds(2 * random.random())

                # 获取当前页面的源码
                text = get_html(url_list[l])
                # 获取当前页面的房屋信息
                data.append(parse_html(text))

                # 反爬随机停止一段时间
                sleep_milliseconds(3 * random.random())  # random.random()随机生成0-1之间的小数
                print('Getting {} item!!'.format(l + 1))
            print('-----Getting {} page!!-----'.format(i + 1))
            # 反爬随机停止一段时间
            sleep_milliseconds(5 * random.random())

            if i % 5 == 0:
                # 每5页保存一次数据
                pd.DataFrame(data).to_excel(filename_excel, encoding='GB18030')
                print('The data from the first {} pages has been saved.'.format(i))
        # 保存数据
        # pd.DataFrame(data).to_csv(filename_csv, encoding='GB18030')
        pd.DataFrame(data).to_excel(filename_excel, encoding='GB18030')
        print('SecondHand-' + q + str(download_times) + 'times_download_finished!!')


start_page = int(input('Please input the start page:'))
end_page = int(input('Please input the end page:'))
download_times = int(input('Please input the download times:'))
myspider([''], start_page, end_page, download_times)
