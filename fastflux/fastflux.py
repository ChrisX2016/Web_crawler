import requests
from bs4 import BeautifulSoup   # use pip install beautifulsoup4
import re
import dns.resolver
import time


class myspider:

    def __init__(self,n):
        self.pageIndex = 1
        self.nLink = n # number of links to get
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
        self.headers = {'User-Agent': self.user_agent}
        self.story = []
        self.enable = False
        self.OKGREEN = '\033[92m'
        self.FAIL = '\033[91m'
        self.WARNING = '\033[93m'
        self.ENDC = '\033[0m'

    def getFirstId(self):
        try:
            url = 'http://www.phishtank.com/phish_search.php?page='+ str(self.pageIndex) +'&active=y&verified=u'
            html = requests.get(url,headers = self.headers)
            soup = BeautifulSoup(html.text, 'html.parser')
            firstId = soup.tr.next_sibling.next_sibling.td.a.get_text()
            return int(firstId)
        except requests.ConnectionError as e:
            print(self.FAIL + str(e) + self.ENDC)
            return None

    def exportLinks(self,links):
        with open('aaa','w') as f:
            for content in links:
                f.write(content+'\n')

    def getLinks(self,firstId):
        i = 0
        links=[]
        while(i < self.nLink):
            url = 'http://www.phishtank.com/phish_detail.php?phish_id=' + str(firstId-i)
            html = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(html.text, 'html.parser')
            link = soup.find("div", { "class" : "url" }).next_sibling.next_sibling.get_text()
            links.append(str(firstId-i) + link.strip())
            i += 1
            if i % 20 == 0:
                print(self.OKGREEN+ '-----Get PhishingSites ' + str(i)+'/'+ str(self.nLink)+ self.ENDC)
        return links

    def start(self):
        firstId = self.getFirstId()
        links = self.getLinks(firstId)
        self.exportLinks(links)
        print(self.OKGREEN + '-----Get PhishingSites Done' + self.ENDC)


class FastFlux:
    def __init__(self,mins):
        self.mins = mins
        self.domains = []
        self.keyToDel = []
        self.OKGREEN = '\033[92m'
        self.FAIL = '\033[91m'
        self.WARNING = '\033[93m'
        self.ENDC = '\033[0m'
        self.OKBLUE = '\033[94m'
        self.suffix = 'com|net|cl|pl|hu|co|ru|by|org|cc|cn'

    def getLinks(self):
        with open('PhishingSites','r') as f:
            links = f.readlines()
        return [x.strip() for x in links]

    def getDomain(self,link,resolver_res):
        link+='/'
        patString = r'(\d{7})(?:http://|https://)(.*?)/'
        pattern = re.compile(patString)
        match = pattern.search(link)
        if match:
            nr = match.groups()
            id = nr[0]
            url = nr[1]
            # print(url)
            patString2 = r'.*\.([\w-]+\.(?:'+self.suffix+'))'
            pattern2 = re.compile(patString2)
            nr2 = pattern2.match('.'+url)
            if nr2:
                domain = nr2.group(1)
                if domain not in self.domains:
                    self.domains.append(domain)
                    resolver_res[id]={'link':link[7:-1],'domain':domain}
            else:
                print(self.WARNING + 'add suffix to self.suffix variable ' + url + " " + link + self.ENDC)
            return
        else:
            print(self.FAIL +'can not extract domian ' + link + self.ENDC)

    def getAandNS(self,resolver_res,key):
        domainName = resolver_res[key]['domain']
        print("Processing " + domainName)
        try:
            answers = dns.resolver.query(domainName, 'A')
            ipA = []
            for rdata in answers:
                ipA.append(rdata.to_text())
            resolver_res[key]['A']=ipA
        except Exception as e:
            print(self.FAIL + str(e) + self.ENDC)
            self.keyToDel.append(key)
            return
        try:
            answers2 = dns.resolver.query(domainName, 'NS')
        except Exception as e:
            print(self.FAIL + str(e) + self.ENDC)
            self.keyToDel.append(key)
            return
        NS={}
        for nameserver in answers2:
            nameserver.to_text()
            try:
                answers2 = dns.resolver.query(nameserver.to_text(), 'A')
                NS[nameserver.to_text()]=[]
                for ipaddress in answers2:
                    NS[nameserver.to_text()].append(ipaddress.to_text())
            except Exception as e:
                print(self.FAIL + str(e) + self.ENDC)
        resolver_res[key]['NS']=NS

    def compare(self,resolver_res,check_resovler_res):
        # print(check_resovler_res)
        key_fastflux = []
        for key in check_resovler_res:
            # print(check_resovler_res[key])
            ipA_check = check_resovler_res[key]['A']
            ipA = resolver_res[key]['A']
            for i in ipA_check:
                if i not in ipA:
                    key_fastflux.append(key)
            NS_check = check_resovler_res[key]['NS']
            NS = resolver_res[key]['NS']
            IPs = []
            for ip in NS.values():
                IPs+=ip
            for ip_check in NS_check.values():
                for x in ip_check:
                    if x not in IPs:
                        key_fastflux.append(key)
                        break

            # for NS_name in NS_check:
            #     IPs = []
            #     for ip in NS[NS_name].itervalues():
            #         IPs.append(ip)
            #
            #     for ip_check in  NS_check[NS_name].itervalues():
            #         if ip_check not in IPs:
            #             key_fastflux.append(key)
            #             break
        return key_fastflux

    def exportRes(self,key,resolver_res,check_resovler_res):
        with open('SuspectFastFlux', 'a') as f:
            domain = check_resovler_res[key]['domain']
            f.write("---------- id: " + key + " domain: " + domain + "\nlink: " + check_resovler_res[key]['link'] + "\n")
            for x in resolver_res[key]['A']:
                f.write(domain + " A " + x + "\n")
            f.write("NS information" + "\n")
            for key2,value in resolver_res[key]['NS'].items():
                f.write(key2 + " A " + ', '.join(value) + "\n")
            f.write("Check with in "+str(self.mins) + " mins\n")
            for x in check_resovler_res[key]['A']:
                f.write(domain + " A " + x + "\n")
            f.write("NS information"+ "\n")
            for key3,value in resolver_res[key]['NS'].items():
                f.write(key3 + " A " + ', '.join(value) + "\n")
            f.write("\n")
            resolver_res[key] = check_resovler_res[key]

    def start(self):
        resolver_res = {}
        links = self.getLinks()
        for link in links:
            self.getDomain(link,resolver_res)
        # print(resolver_res)
        for key in resolver_res:
            self.getAandNS(resolver_res, key)
        print(self.OKBLUE + "-----Remove fault domian"+ self.ENDC)
        for key2 in self.keyToDel:
            del resolver_res[key2]
        print(self.OKGREEN+ "-----Get IP, NS, NS's IP DONE"+ self.ENDC)
        print(resolver_res)
        # i = 1
        # while (1):
        print(self.OKBLUE + "-----Wait " + str(self.mins) + " mins" + self.ENDC )
        time.sleep(self.mins*60)
        check_resovler_res = {}
        for key in resolver_res:
            check_resovler_res[key] = {'domain':resolver_res[key]['domain'],'link':resolver_res[key]['link']}
        for key in check_resovler_res:
            self.getAandNS(check_resovler_res, key)
            # print(check_resovler_res)
        key_fastflux = self.compare(resolver_res,check_resovler_res)
        key_fastflux = list(set(key_fastflux))
        print(key_fastflux)
        if key_fastflux:
            print(self.OKGREEN+"-----Found suspect fastflux, start to export"+ self.ENDC)
            for x in key_fastflux:
                self.exportRes(x,resolver_res,check_resovler_res)
            print(self.OKGREEN + "-----Export Done" + self.ENDC)
        else:
            print(self.OKBLUE + "-----No suspect fastflux" + self.ENDC)
            # i+=1


NLINKS = 200 # number of PhishingSites to get
MINS = 5 # time interval for check

spider = myspider(NLINKS)
spider.start()

test = FastFlux(MINS)
test.start()

