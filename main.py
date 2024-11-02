import requests
response=requests.get('https://www.sdu.edu.cn/index.htm')
print(response.text.encode('utf-8'))
