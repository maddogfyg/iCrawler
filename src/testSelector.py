#!/usr/bin/env python
#coding=utf-8

import unittest
from BeautifulSoup import BeautifulSoup
from BTSelector import findAll,tokenize,checkTokenType

class SelectorTester(unittest.TestCase):
    def testTokenize(self):
        target = ' div .attr  #ok '
        ret = []
        for token in tokenize(target):
            ret.append(token)
        self.assertEqual(3,len(ret))
        
    def testCheckTokenType(self):
        self.assertEqual('class',checkTokenType('.name'))
        self.assertEqual('id',checkTokenType('#name'))
        self.assertEqual('tag',checkTokenType('div'))
        self.assertEqual('tag',checkTokenType('div#name'))
        self.assertEqual('op',checkTokenType('+'))
        self.assertEqual('op',checkTokenType('>'))
    
    def testTag(self):
        target = "h3"
        soup = BeautifulSoup("<h1>hello</h1><h3>heyhey</h3>")
        ret = findAll(target,soup)
        self.assertEqual(1,len(ret))
        
    def testTagWithAttrs(self):
        target = "div.item#one[width=100]"
        html = '''
        <div class="item" id="one" width="100">
            hey
        </div>
        <div class="item" id="two">
            man,
        </div>
        <div class="the">
            fuckup
        </div>
        '''
        soup = BeautifulSoup(html)
        ret = findAll(target,soup)
        self.assertEqual(1,len(ret))
        
    def testMoreTag(self):
        target = 'div.share .my'
        html = '''
        <div class="share">
            <a class="my" href="#"></a>
            <a class="your" href="#">OK</a>
        </div>
        '''
        soup = BeautifulSoup(html)
        ret = findAll(target,soup)
        self.assertEqual(1,len(ret))
        
    def testClass(self):
        target = ".item"
        soup = BeautifulSoup('<a class="iwill" href="#"></a><a class="item" href="#">hello</a><img class="item" src="cc.png"/>')
        ret = findAll(target,soup)
        self.assertEqual(2,len(ret))
        
    def testId(self):
        target = "#header"
        soup = BeautifulSoup('<div id="header">hey</div><div id="hello">you</div>')
        ret = findAll(target,soup)
        self.assertEqual(1,len(ret))
    
    def testPosition(self):
        target = "h2 + ul > li > a"
        html = '''
        <h2>title</h2>
        <ul>
            <li><a href="#">nothing</a></li>
            <li><a href="#">ok</a></li>
            <li><a href="#">come on!</a></li>
        </ul>
        '''
        soup = BeautifulSoup(html)
        ret = findAll(target,soup)
        self.assertEqual(3,len(ret))
        
    def testMixSelection(self):
        target = "#header > div#name > a.highlight"
        html = '''
        <div id="header">
            <div id="name">
                <a class="target">test</a>
                <a class="highlight">right</a>
                <a class="highlight">ok</a>
            </div>
            <div id="your">
            </div>
        </div>
        <div id="body">fk
        </div>
        '''
        soup = BeautifulSoup(html)
        ret = findAll(target,soup)
        self.assertEqual(2,len(ret))

if __name__ == "__main__":
	unittest.main()
