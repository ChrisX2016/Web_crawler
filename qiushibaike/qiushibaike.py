import requests
from bs4 import BeautifulSoup


# page = 1
# user_agent = 'User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64)'
# headers = {'User-Agent':user_agent}
#
# url = 'http://www.qiushibaike.com/hot/page/' + str(page)
#
# html = requests.get(url,headers = headers)
#
# soup = BeautifulSoup(html.text,'html.parser')
# Content = soup.findAll('div',{'class':'content'})
# print(Content[0].text)

class QSBK:

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
        self.headers = {'User-Agent': self.user_agent}
        self.story = []
        self.enable = False

    def getStory(self):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(self.pageIndex)
            html = requests.get(url,headers = self.headers)
            soup = BeautifulSoup(html.text, 'html.parser')
            content = soup.findAll('div', {'class': 'content'})
            return content
        except requests.ConnectionError as e:
            print(e.reason)
            return None


    def load(self):
        if self.enable == True:
            if len(self.story) < 2:
                stories = self.getStory()
                if stories:
                    self.story += stories
                    self.pageIndex += 1


    def printStory(self,count):
        inputt = input()
        if inputt == 'q':
            self.enable = False
            return
        print('count: %s\nstory: %s'%(count,self.story[0].text))

    def start(self):
        self.enable = True
        self.load()
        count = 0
        while self.enable:
            if len(self.story)>0:
                count += 1
                self.load()
                self.printStory(count)
                del self.story[0]

spider = QSBK()
spider.start()
