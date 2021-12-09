import re
import pandas
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

def get_html(url):
    try:
        r = requests.get(url)               # 使用get来获取网页数据
        r.raise_for_status()                # 如果返回参数不为200，抛出异常
        r.encoding = r.apparent_encoding    # 获取网页编码方式
        return r.text                       # 返回获取的内容
    except:
        return '错误'

def save(html):

    # 解析网页
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)

    with open('./data/B_data.txt', 'r+', encoding='UTF-8') as f:
        f.write(soup.text)

    name = []    # 动漫名字
    hua = []     # 更新话数
    bfl = []     # 播放量
    zf = []      # 追番数
    pjbfl = []   # 平均每话播放量

    # ********************************************  动漫名字存储
    for tag in soup.find_all('div', class_='info'):
        # print(tag)
        bf = tag.a.string
        name.append(str(bf))
    print(name)

    # ********************************************  更新话数
    for tag in soup.find_all('div', class_='detail'):
        # print(tag)
        bf = tag.find('span', class_='data-box').get_text()
        bf = float(re.search(r'\d*(\.)?\d', bf).group())
        hua.append(float(bf))
    print(hua)

    # ********************************************  播放量存储
    for tag in soup.find_all('div', class_='detail-state'):
        # print(tag)
        bf = tag.find('span', class_='data-box').get_text()
        if '亿' in bf:
            num = float(re.search(r'\d(.\d)?', bf).group()) * 10000
            # print(num)
            bf = num
        else:
            bf = re.search(r'\d*(\.)?\d', bf).group()
        bfl.append(float(bf))
    print(bfl)

    # ********************************************  系列追番数
    for tag in soup.find_all('div', class_='detail-state'):
        bf = tag.find('span', class_='data-box').next_sibling.next_sibling.get_text()
        bf = re.search(r'\d*(\.)?\d', bf).group()
        zf.append(float(bf))
    print(zf)

    # 数据分析
    # ********************************************  平均每话播放量
    pjbfl = np.divide(bfl, hua)
    print(pjbfl)

    # 存储至excel表格中
    info = {'动漫名': name, '更新话数(话)': hua, '播放量(万)': bfl, '平均每话播放量(万)': pjbfl, '追番数(万)': zf}
    dm_file = pandas.DataFrame(info)
    dm_file.to_excel('Bilibili.xlsx', sheet_name="动漫数据分析")
    # 将所有列表返回
    return name, hua, bfl, zf, pjbfl


def view(info):
    my_font = font_manager.FontProperties(fname='./data/STHeiti Medium.ttc')  # 设置中文字体
    dm_name = info[0]
    dm_episode = info[1]
    dm_play = info[2]
    dm_follow = info[3]
    dm_average = info[4]

    # 为了坐标轴上能显示中文
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 图像绘制
    # **********************************************************************播放量
    # *******播放量柱状图
    fig, ax1 = plt.subplots()
    ax1.stem(dm_name, dm_play)
    plt.title('播放量数据分析', fontproperties=my_font)
    ax1.tick_params(labelsize=6)
    plt.xticks(rotation=90, color='grey')
    plt.ylabel('播放量（万）')
    plt.xlabel('番剧名')

    plt.savefig(r'C:\Users\90643\Desktop\Python-Bilibili\1.png', dpi=1000, bbox_inches='tight')

    # **********************************************************************更新话数和播放量对比
    # *******更新话数条形图
    fig, ax2 = plt.subplots()
    plt.bar(dm_name, dm_episode, color='plum')
    plt.title('更新话数和播放量数据分析', fontproperties=my_font)
    ax2.tick_params(labelsize=6)
    plt.xlabel('番剧名')
    plt.ylabel('更新话数（话）')
    plt.xticks(rotation=90, color='gold')

    # *******播放量折线图
    ax3 = ax2.twinx()  # 组合图必须加这个
    ax3.plot(dm_play, color='skyblue')  # 设置线粗细，节点样式
    plt.ylabel('播放量（万）')

    plt.plot(1, label='更新话数', color="plum", linewidth=5.0)
    plt.plot(1, label='播放量', color="skyblue", linewidth=1.0, linestyle="-")
    plt.legend()

    plt.savefig(r'C:\Users\90643\Desktop\Python-Bilibili\2.png', dpi=1000, bbox_inches='tight')

    # **********************************************************************平均每话播放量
    # *******平均每话播放量水平柱状图
    fig, ax4 = plt.subplots()
    ax4.barh(dm_name, dm_average, height=0.7, align='center', color='pink')
    ax4.tick_params(labelsize=6)
    plt.title('平均每话播放量数据分析', fontproperties=my_font)
    plt.yticks(rotation=10, color='k')
    plt.ylabel('番剧名')
    plt.xlabel('平均每话播放量（万）')

    plt.savefig(r'C:\Users\90643\Desktop\Python-Bilibili\3.png', dpi=1000, bbox_inches='tight')

    # **********************************************************************平均每话播放量和播放量对比
    # ********平均每话播放量数折线图
    fig, ax5 = plt.subplots()
    plt.plot(dm_name, dm_average, color='turquoise')
    plt.title('平均每话播放量数和播放量数分析')
    plt.ylabel('平均每话播放量（万）')
    ax5.tick_params(labelsize=6)
    plt.xticks(rotation=90, color='green')

    # *******播放量数折线图
    ax6 = ax5.twinx()  # 组合图必须加这个
    ax6.plot(dm_play, color='gold')  # 设置线粗细，节点样式
    plt.ylabel('播放量（万）')

    plt.plot(1, label='平均每话播放量', color="turquoise", linewidth=1.0, linestyle="-")
    plt.plot(1, label='播放量', color="gold", linewidth=1.0, linestyle="-")
    plt.legend()

    plt.savefig(r'C:\Users\90643\Desktop\Python-Bilibili\4.png', dpi=1000, bbox_inches='tight')

    # # **********************************************************************追番人数和播放量对比
    # *******追番人数条形图
    fig, ax7 = plt.subplots()
    plt.bar(dm_name, dm_follow, color='lightgreen')
    plt.title('追番人数和播放量数据分析')
    plt.ylabel('追番人数（万）')
    ax7.tick_params(labelsize=6)
    plt.xticks(rotation=90, color='darkviolet')

    # *******播放量折线图
    ax8 = ax7.twinx()  # 组合图必须加这个
    ax8.plot(dm_play, color='salmon')  # 设置线粗细，节点样式
    plt.ylabel('播放量（万）')
    plt.plot(1, label='追番人数', color="lightgreen", linewidth=5.0)
    plt.plot(1, label='播放量', color="salmon", linewidth=1.0, linestyle="-")
    plt.legend()

    plt.savefig(r'C:\Users\90643\Desktop\Python-Bilibili\5.png', dpi=1000, bbox_inches='tight')

    plt.show()


def main():
    # 国产动画排行榜分析
    # url = 'https://www.bilibili.com/v/popular/rank/guochan'
    # 番剧排行榜分析
    url = 'https://www.bilibili.com/v/popular/rank/bangumi'
    # 电视剧排行榜分析
    # url = 'https://www.bilibili.com/v/popular/rank/tv'
    html = get_html(url)
    info = save(html)
    view(info)


if __name__ == '__main__':
    main()