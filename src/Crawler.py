from sys import argv
from os import makedirs, unlink, sep
from os.path import isdir, exists, dirname, splitext
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin
from formatter import DumbWriter, AbstractFormatter
from io import StringIO
import configparser
import re
import urllib
from myParser import myParser
import sqlite
import time


class Crawler():        # manage entire crawling process

    count = 0            # static downloaded page counter
    def __init__(self):
        self.seen = []
        
    def go(self):                # process links in queue
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        startUrl = conf.get('crawler', 'startUrl')
        self.divClass = conf.get('crawler', 'divClass')
        nofollowStr = conf.get('crawler', 'nofollow')
        self.nofollowList = nofollowStr.split(",")
        intervalSeconds = int(conf.get("crawler","intervalSeconds"))
        startUrl = conf.get("crawler","startUrl")
        urlLs = conf.get("crawler","urlLs")
        
        self.domainName = self.getDomainName(startUrl)
        self.linkQueue = ["http://" + self.domainName, "http://" + self.domainName + '/']
        self.linkDone = []
        while self.linkQueue:
            url = self.linkQueue.pop()
            self.linkDone.append(url)
            print('>>>Now start parse '+url)
#            self.parsePage(url)
            try:
                self.parsePage(url)
            except Exception as e:
                fError = open('../error.log', 'a+')
                fError.write(url+'\n'+str(e)+'\n\n')
                print(url+'\n'+str(e)+'\n\n')

            time.sleep(intervalSeconds)


    
    def parsePage(self, url):
        webpageBytes = urllib.request.urlopen(url).read()
        gbkCharset = re.compile('charset\s*=\s*(gb2312|gbk)',re.IGNORECASE)
        mGbk = re.search(gbkCharset, str(webpageBytes))
        if mGbk is not None:
            webpage = webpageBytes.decode('gbk','ignore')
        else:
            utf8Charset = re.compile('charset\s*=\s*utf-8',re.IGNORECASE)
            mUtf8 = re.search(utf8Charset, str(webpageBytes))
            if mUtf8 is not None:
                webpage = webpageBytes.decode('utf-8','ignore')
            else:
                webpage = webpageBytes.decode('gbk','ignore')
    #===============================================================================
    #    webpage = re.sub(r"\\'", r"'", webpage)
    #    webpage = re.sub(r'\\[rn]', r' ', webpage)
    #===============================================================================
        webpage = re.sub('\s+',' ', webpage)
        
        doubleQuotation = re.compile(r'("[^=><"]*)"([^=><"]*)"([^=><"]*")')
        oldList = doubleQuotation.findall(webpage)
        for oldItem in oldList:
            webpage = webpage.replace(oldItem[0]+'"'+oldItem[1]+'"'+oldItem[2], oldItem[0]+"'"+oldItem[1]+"'"+oldItem[2])
        
        tp = myParser(self.divClass)
        tp.feed(webpage)
        newlink = ''
        for newlink in tp.getlinklist():
            noFollow = 0 
            for nf in self.nofollowList:
                if newlink.find(nf) != -1:
                    noFollow = 1
            if noFollow:
                continue
            if str.find(str.lower(newlink), 'mailto:') != -1:
                continue
            #other domain
            if newlink[:7] == 'http://' and newlink.find(self.domainName) == -1:
                continue
#some links like 'www.xxx.com', then the final link would be 'http://www.abc.com/www.xxx.com, error!
            if newlink[:7] != 'http://' and newlink[0] != '/':
                continue
            if newlink[:4] != 'http' and newlink.find('://') == -1:
                newlink = 'http://'+self.domainName+newlink
            if newlink not in self.linkQueue and newlink not in self.linkDone:
                self.linkQueue.append(newlink)
                print(newlink)

        if len(tp.getcontent()) == 0:
            fNothing = open('../nocontent.log','a+')
            fNothing.write(url+'\n')
            print("nothing!")
            return None
        sqlitehandle = sqlite.sqlite()
        sqlitehandle.insertContent(url, tp.gettitle(), tp.getcontent() )
#===============================================================================
#        f = open('../content.txt', 'a+')
#        f.write(url+'\n')
#        f.write(tp.gettitle()+'\n')
#        f.write(tp.getcontent()+'\n\n')
#===============================================================================
        print(tp.gettitle())
        print(tp.getcontent())

        
    def updatePriQueue( priQueue, url ):
        extraPrior = url.endswith('.html') and 2 or 0 #download urls which ended with html first
        extraMyBlog = 'www.itangyou.com' in url and 5 or 0 #
        item = priQueue.getitem(url)
        if item :
            newitem = ( item[0]+1+extraPrior+extraMyBlog, item[1] )
            priQueue.remove(item)
            priQueue.push( newitem )
        else :
            priQueue.push( (1+extraPrior+extraMyBlog,url) )

    def getDomainName(self,url):
        "get the website address of the url, and add it to the relative address url"
        ix = url.find('/')
        if ix > 0 :
            return url[:ix]
        else :
            return url
    
    def analyseHtml(url,html, priQueue,downlist):
        p = Parser()
        try :
            p.feed(html)
            p.close()
        except:
            return
        
        mainurl = getmainurl(url)
    
        for k, v in p.anchors.items():
            for u in v :
                if not u.startswith('http://'):  #handle the relative address url
                    u = mainurl + u       
                if not downlist.count(u) :    #if the url has been downloaded, pass
                    updatePriQueue( priQueue, u )
    
    def downloadUrl(id, url, priQueue , downlist,downFolder):
        "download the url, and analize the html"
        downFileName = downFolder+'/%d.html' % (id,)
        print('downloading',url,'as', downFileName ,)
    
        try:
            fp = urllib.request.urlopen(url)
        except:
            print('[ failed ]')
            return False
    
        else :
    
            print('[ success ]')
            downlist.push( url )  #add the downloaded urls to list
            op = open(downFileName,"wb")
            html = fp.read()
            op.write( html )
            op.close()
            fp.close()        
            analyseHtml(url,html,priQueue,downlist)
            return True

    def spider(beginurl, pages,downFolder):
        priQueue = PriorityQueue()
        downlist = PriorityQueue() #the urls downloaded, to prevent download several times
        priQueue.push( (1,beginurl) )
        i = 0
        while not priQueue.empty() and i < pages :
            k, url = priQueue.pop()
            if downloadUrl(i+1, url, priQueue , downlist,downFolder):
                i += 1
        print('\nDownload',i,'pages, Totally.')
