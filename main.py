import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from urllib.parse import urljoin
import jieba
from wordcloud import WordCloud
import os

data1 = []
data2 = []
url1 = 'https://www.bkjx.sdu.edu.cn/index/gztz.htm'
url2 = 'https://www.cs.sdu.edu.cn/bkjy.htm'


# 获取通知内容
def get_content1(link):
    response = requests.get(link).content.decode('utf-8', errors='ignore')
    soup = BeautifulSoup(response, 'html.parser')
    content = soup.find('div', class_='v_news_content')
    if content:
        return content.text.strip()  # 去除字符串两端的空白字符（包括空格、制表符、换行符等
    else:
        return ""


def get_content2(link):
    response = requests.get(link).content.decode('utf-8', errors='ignore')
    soup = BeautifulSoup(response, 'html.parser')
    content = soup.find('div', class_='v_news_content')
    if content:
        return content.text.strip()
    else:
        return ""


# 获取标题，链接，时间
def get_title_link1(url):
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    chapters = soup.find('div', class_='newscontent')
    if chapters:
        chapters = chapters.find_all('a')
        for each in chapters:
            time0 = each.parent.find_next_sibling()
            if time0:
                time = time0.text
                title = each.text
                link = urljoin(url, each.get('href'))
                data1.append([title, time, link])
        return data1
    else:
        raise ValueError("未找到章节列表，请检查页面结构")


def get_title_link2(url):
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    chapters = soup.find('div', class_='dqlb')
    if chapters:
        chapters = chapters.find_all('a')
        for each in chapters:
            time0 = each.parent.find_next_sibling()
            if time0:
                time = time0.text
                title = each.text
                link = urljoin(url, each.get('href'))
                data2.append([title, time, link])
        return data2
    else:
        raise ValueError("未找到章节列表，请检查页面结构")


# 生成词云图
def create_word_cloud(text, filename):
    for ch in ':。，/？‘’【】{}、|;?, -\'''年''月''日':
        text = text.replace(ch, "")
    words = jieba.cut(text)
    stopwords = set()
    with open('stop_words_CHN.txt', 'r', encoding='utf-8') as f:
        stopwords.update(f.read().splitlines())

    # 去除停用词
    text = ' '.join([word for word in words if word not in stopwords])

    # 生成词云
    wc = WordCloud(font_path="/Fonts/simhei.ttf", background_color="white")
    wc.generate(text)

    # 保存词云图像
    wc.to_file(filename)


def main():
    # 创建一个文件夹来存放所有通知的内容和词云图
    base_output_dir1 = "本科生院通知文件"
    os.makedirs(base_output_dir1, exist_ok=True)  # 创建主目录1
    base_output_dir2 = "计科通知文件"
    os.makedirs(base_output_dir2, exist_ok=True)  # 创建主目录2

    # 打开文件
    wb1 = Workbook()
    ws1 = wb1.active
    ws1.title = "本科生院工作通知"
    ws1.append(["标题", "时间", "链接"])
    ws1.column_dimensions["A"].width = 120
    ws1.column_dimensions["B"].width = 20
    ws1.column_dimensions["C"].width = 80

    title_link_data1 = get_title_link1(url1)

    wb2 = Workbook()
    ws2 = wb2.active
    ws2.title = "计科工作通知"
    ws2.append(["标题", "时间", "链接"])
    ws2.column_dimensions["A"].width = 120
    ws2.column_dimensions["B"].width = 20
    ws2.column_dimensions["C"].width = 80

    title_link_data2 = get_title_link2(url2)

    for title1, time1, link1 in title_link_data1:
        ws1.append([title1, time1, link1])
        print(title1)

        # 获取每个通知内容
        content1 = get_content1(link1)

        # 创建对应的子文件夹
        notification_dir1 = f"{base_output_dir1}/{title1}"
        os.makedirs(notification_dir1, exist_ok=True)  # 创建子文件夹

        # 将内容写入相应的的.txt 文件
        filename_txt1 = f"{notification_dir1}/{title1}.txt"
        with open(filename_txt1, "w", encoding='utf-8') as f1:
            f1.write(content1)

        # 生成对应的词云图
        wordcloud_filename1 = f"{notification_dir1}/{title1}_wordcloud.png"
        create_word_cloud(content1, wordcloud_filename1)

    wb1.save("本科生院官网通知.xlsx")  # 将标题，时间，链接存在excel中

    for title2, time2, link2 in title_link_data2:
        ws2.append([title2, time2, link2])
        print(title2)

        # 获取每个通知内容
        content2 = get_content2(link2)

        # 创建对应的子文件夹
        notification_dir2 = f"{base_output_dir2}/{title2}"
        os.makedirs(notification_dir2, exist_ok=True)  # 创建子文件夹

        # 将内容写入相应的的.txt 文件
        filename_txt2 = f"{notification_dir2}/{title2}.txt"
        with open(filename_txt2, "w", encoding='utf-8') as f2:
            f2.write(content2)

        # 生成对应的词云图
        if content2:
            wordcloud_filename2 = f"{notification_dir2}/{title2}_wordcloud.png"
            create_word_cloud(content2, wordcloud_filename2)

    wb2.save("计科官网通知.xlsx")  # 将标题，时间，链接存在excel中


if __name__ == "__main__":
    main()
