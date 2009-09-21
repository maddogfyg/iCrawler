import html.parser
import re

class myParser(html.parser.HTMLParser):
    '''
    Parse the Webpage
    '''
    def __init__(self, className):
        self.className = className
        self.title, self.content = '', ''
        self.isTitle, self.isLink, self.isScript, self.isContent = 0, 0, 0, 0
        self.linklist = []
        html.parser.HTMLParser.__init__(self)

    def handle_starttag(self,tag,attrs):
        if tag=='title':
            self.isTitle=1
        if tag=='script':
            self.isScript=1
        if tag=='a':
            self.isLink=1
            for attr in attrs:
                if attr[0]=='href':
                    self.linklist.append(attr[1])

        for attr in attrs:
            if attr[0]=='class' and attr[1]==self.className:
                self.isContent=1

    def handle_data(self,data):
        if self.isTitle:
            self.title += data
        if self.isLink or self.isScript:
            return
        if self.isContent:
            self.content += data

    def handle_endtag(self,tag):
        if tag=='title':
            self.isTitle=0
        if tag=='a':
            self.isLink=0
        if tag=='script':
            self.isScript=0
        #we assume that all content would be in one div district
        if tag=='div':
            self.isContent=0

    def handle_comment(self,data):
        if data.find('/content') != -1:
            self.isContent=0

    def gettitle(self):
        return self.title
    
    def getcontent(self):
        return self.content
    
    def getlinklist(self):
        return self.linklist


