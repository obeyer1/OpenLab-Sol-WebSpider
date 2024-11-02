
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
url="https://www.rsrczp.sdu.edu.cn/info/1053/6132.htm"
response=requests.get(url)
html=response.content.decode("utf-8")
soup=BeautifulSoup(html,"html.parser")
content=soup.find("div",class_="neirong").text
file=open(r"F:\python\通知\新建 文本文档.txt","w",encoding="utf-8")
file.write(content)
file.close()
w=WordCloud(font_path="/Fonts/simhei.ttf").generate(content)
w.to_file(r"F:\图片\wordcloud.png")
print(content)
print(url)
