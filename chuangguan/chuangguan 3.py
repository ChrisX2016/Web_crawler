import requests
import re
url1 = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/'
url2 = 'http://www.heibanke.com/lesson/crawler_ex02/'
temp = requests.session()
temp.get(url1)
token = temp.cookies['csrftoken']

index = 0
data= {'username':'admin','password':123456,'csrfmiddlewaretoken':token}
temp.post(url1,data)
sol = 1

temp.get(url2)
token = temp.cookies['csrftoken']
data= {'username':'admin','password':0,'csrfmiddlewaretoken':token}

while sol:
    index += 1
    data['password'] = index
    html = temp.post(url2,data).text
    sol = re.findall(r'密码错误',html)
    print(index)

print(index,html)

