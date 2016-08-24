import requests
import re
from threading import Thread
import time

url1 = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex03/'
url2 = 'http://www.heibanke.com/lesson/crawler_ex03/'
url3 = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/'

temp = requests.session()
temp.get(url1)
token  = temp.cookies['csrftoken']
data = {'username':'admin','password':'123456','csrfmiddlewaretoken':token}
temp.post(url1,data)

temp.get(url2)
token = temp.cookies['csrftoken']
data['csrfmiddlewaretoken'] = token

password={}

def loop(passwd):
    html = temp.get(url3)
    pos = re.findall(r'password_pos">([0-9]*)</td>',html.text)
    val = re.findall(r'password_val">([0-9]*)</td>',html.text)
    for i in range(len(pos)):
        # if val[i] not in passwd:
        passwd[int(pos[i]) - 1] = val[i]
    print(passwd)
    print(len(passwd))

passwd = ['' for i in range(100)]
T = ['t1','t2']
while '' in passwd:
    for t in T:
        t = Thread(target=loop(passwd))
        t.start()
        time.sleep(8)
    for i in T:
        t.join()

passwd = ''.join(passwd)
print(passwd)
