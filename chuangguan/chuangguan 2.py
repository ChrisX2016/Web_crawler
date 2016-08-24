import requests
import re

url = "http://www.heibanke.com/lesson/crawler_ex01/"
# url = "https://www.baidu.com/"
index = 0
data = {'username':'admin'}
sol = 1

while sol:
    data['password'] = index
    html = requests.post(url, data).text
    print(type(html))
    sol = re.findall(r'密码错误', html)
    index += 1
    print(index)

print(html, index - 1)

