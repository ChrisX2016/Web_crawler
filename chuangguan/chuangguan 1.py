import urllib.request
import re

url = "http://www.heibanke.com/lesson/crawler_ex00/"
data = urllib.request.urlopen(url).read()
data = data.decode('UTF-8')
index = re.findall(r'数字([\d]{5})', data)

while index:
    url = "http://www.heibanke.com/lesson/crawler_ex00/%s/" % index[0]
    data = urllib.request.urlopen(url).read()
    data = data.decode('UTF-8')
    index = re.findall(r'数字是([\d]{5})', data)

print(data)