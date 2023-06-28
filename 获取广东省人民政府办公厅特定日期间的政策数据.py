import requests
import json
import datetime
from lxml import etree
import time
import random
headers = {
    "User-Agent": "浏览器信息"
}

# datalist用于存放满足要求的数据，包含索引号、发布机构、发布日期、政策标题、政策正文文本、政策正文附件链接，以上六项信息
datalist = []


def main():
    # 广东省人民政府办公厅政府信息公开平台url 页码范围 1-237
    url = r"http://www.gd.gov.cn/gkmlpt/api/all/5?page="

    # 1.输入日期范围  例：(20220101-20230601)
    d_time = input("请输入日期范围 例: 20220101-20230601: ")
    start = d_time.split('-')[0]
    end = d_time.split('-')[1]
    # print(start)
    # print(end)

    # 将日期转换为时间戳
    start_time = datetime.datetime.strptime(start, "%Y%m%d").timestamp()
    end_time = datetime.datetime.strptime(end, "%Y%m%d").timestamp()
    # print(int(start_time))
    # print(int(end_time))

    # 2.拼接页码，获取数据,页码范围 1-237
    for i in range(1, 237):
        # print(url + str(i))
        print(f'正在获取第{i}页数据')
        resp = requests.get(url + str(i), headers=headers)
        # 将Unicode编码解码为中文
        s = resp.content.decode("unicode-escape")
        # print(s)
        # 将JSON数据转换为Python对象，通过字典key来访问
        data = json.loads(s)
        # 获取数据，并将数据添加到datalist中
        jx_data(data, start_time, end_time)
        # 每爬一页让程序随机休眠一段时间，避免触发反爬机制
        time.sleep(random.randint(5,10))

    # 3.输出数据
    print_data()


# --------------------------------------------------------分割线---------------------------------------------------------

# 查传入政策详情链接的正文和附件链接并将其返回
def zw_fj(url):
    resp = requests.get(url, headers=headers)
    # print(resp.text)
    html = etree.HTML(resp.text)
    # 正文
    divs = html.xpath("/html/body/div[2]/div[4]/div[3]/div[3]/div[2]/p/text()")
    zw = ''.join(divs)
    # print(zw)
    # 附件url
    try:
        fujian_url = html.xpath("/html/body/div[2]/div[4]/div[3]/div[3]/div[2]/p/a/@href")[0]
    except:
        fujian_url = None
    # print(fujian_url)
    return zw, fujian_url


# 传入data字典，起始时间戳，进行数据解析，并将获取的数据加入到datalist中
def jx_data(data, start_time, end_time):
    list = []
    for item in data['articles']:
        # 获取当前政策的发布日期并将其转换为时间戳
        timestamp = datetime.datetime.strptime(item['created_at'], "%Y-%m-%d %H:%M:%S").timestamp()
        # 比较时间戳，满足要求则将数据加入到datalist中
        if start_time <= timestamp <= end_time:
            # 将索引号添加到list中
            # print(item['identifier'])
            list.append(item['identifier'])
            # 将发布机构添加到list中
            # print(item['publisher'])
            list.append(item['publisher'])
            # 将发布日期添加到list中
            # print(item['created_at'])
            list.append(item['created_at'])
            # 将政策标题添加到list中
            # print(item['title'])
            list.append(item['title'])

            # 传入政策详情链接，获取正文内容和附件链接
            # print(item['url'])
            zw, fujian_url = zw_fj(item['url'])
            # 将正文内容添加到list中
            list.append(zw)
            # 将附件链接添加到list中
            list.append(fujian_url)
            # 将list加入到datali中
            datalist.append(list)



# 传入datalist数据集，打印数据 //也可数据持久化
def print_data():
    for li in datalist:
        print('索引号:' + li[0])
        print('发布机构:' + li[1])
        print('发布日期:' + li[2])
        print('政策标题:' + li[3])
        print('正文内容:' + li[4])
        print('附件链接:' + li[5])
        print()


if __name__ == '__main__':
    main()
