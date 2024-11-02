import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import openpyxl
from urllib.parse import urljoin
import jieba
from wordcloud import WordCloud

data = []
url = 'https://www.bkjx.sdu.edu.cn/index/gztz.htm'


def get_content(url):
    response = requests.get(url).content.decode('utf-8', errors='ignore')
    soup = BeautifulSoup(response, 'html.parser')
    content = soup.find('div', class_='v_news_content')
    if content:
        return content.text.strip()  # 使用 .strip() 方法去除首尾的空白字符
        # （如空格、制表符、换行符等）'''
    else:
        return ""


def get_title_link(url):
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    chapters = soup.find('div', class_='newscontent')
    if chapters:
        chapters = chapters.find_all('a')
        for each in chapters:
            time0 = each.parent.find_next_sibling()
            if time0 != None:
                time = each.parent.find_next_sibling().text
                title = each.text
                # print(each.parent.find_next_sibling())
                link = urljoin('https://www.bkjx.sdu.edu.cn/index/gztz.htm', each.get('href'))
                data.append([title, time, link])
        return data
    else:
        raise ValueError("未找到章节列表，请检查页面结构")


def main():
    # 打开文件
    wb = openpyxl.Workbook()  # 创建一个工作簿
    ws = wb.active  # 新的工作簿默认有一个工作表
    ws.title = "本科生院工作通知"  # 设置工作表的标题
    ws.append(["标题", "时间", "链接"])  # 添加表头
    ws.column_dimensions["A"].width = 120  # 设置列宽
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 80
    titlelink = get_title_link(url)
    with open("本科生院官网通知.txt", "w", encoding='utf-8') as f:  # 添加 encoding 参数
        for title, time, link in data:
            ws.append([title, time, link])
            print(title)
            f.write(title + '\n')
            content = get_content(link)
            f.write(content + '\n')

    wb.save("本科生院官网通知.xlsx")
    txt = open("本科生院官网通知.txt", 'r', encoding='utf-8').read()
    for ch in ':。，  /？‘’【】{}、|;'', ?-' '':
        txt = txt.replace(ch, "")
    words = jieba.cut(txt)  # 使用分词工具进行分词
    stopwords = []
    with open(r"E:\Open Lab复试（最终）\stop_words_CHN.txt", 'r', encoding='utf-8') as f:
        stopwords = f.read()

    counts = {}
    for word in words:
        if word not in stopwords:  # 去除停用词
            counts[word] = counts.get(word, 0) + 1  # 使用字典统计词频

    items = list(counts.items())  # 转成列表
    items.sort(key=lambda x: x[1], reverse=True)
    wordStr = ''
    for i in range(50):  # 输出前五十的高频词
        word, count = items[i]
        wordStr += ' ' + word  # 使用空格分隔每一个词汇
        print("{0:<10} {1:>5}".format(word, count))
    w = WordCloud(font_path="/Fonts/simhei.ttf").fit_words(counts)  # 根据词频绘制词云
    w.to_file('通知词云.png')  # 图片放置位置


'''main() 函数只会在脚本直接运行时被调用。如果此脚本被其他脚本导入，
main() 不会被自动执行。这样做的好处是可以方便地复用函数，
同时保证脚本作为独立程序运行时的行为符合预期。'''
if __name__ == "__main__":
    main()



