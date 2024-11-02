import requests
from bs4 import BeautifulSoup

url = 'https://guoxue.httpcn.com/book/xyj/'

def get_content(url):
    response = requests.get(url).content.decode('utf-8', errors='ignore')
    soup = BeautifulSoup(response, 'html.parser')
    content = soup.find('div', class_='contentBox')
    if content:
        return content.text.strip()#'''使用 .strip() 方法去除首尾的空白字符
                                  #（如空格、制表符、换行符等）'''
    else:
        return ""

def get_title_link(url):
    html = requests.get(url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')  # 创建 BeautifulSoup 对象
    chapters = soup.find('div', class_='lunyu_section')  # 查找包含章节的 div
    if chapters:
        chapters = chapters.find_all('a')
        titlelink = {}
        for each in chapters:
            title = each.text
            link = 'https:' + each.get('href')
            titlelink[title] = link
        return titlelink
    else:
        raise ValueError("未找到章节列表，请检查页面结构")

def main():
    titlelink = get_title_link(url)
    with open("爬取西游记.txt", "w", encoding='utf-8') as f:  # 添加 encoding 参数
        for title, link in titlelink.items():
            print(title)
            f.write(title + '\n')
            content = get_content(link)
            f.write(content + '\n')
'''main() 函数只会在脚本直接运行时被调用。如果此脚本被其他脚本导入，
main() 不会被自动执行。这样做的好处是可以方便地复用函数，
同时保证脚本作为独立程序运行时的行为符合预期。'''
if __name__ == "__main__":
    main()
