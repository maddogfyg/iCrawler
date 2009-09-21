# -*- coding: utf-8 -*-
# git+ssh://git@github.com/maddogfyg/iCrawler.git
from PriorityQueue import PriorityQueue
from myParser import myParser
from Crawler import Crawler
import configparser
import getopt
import os
import re
import sqlite
import sys
import time
import urllib
import urllib.request

def main():
    try:
        spider = Crawler()
        spider.go()
    
    except KeyboardInterrupt:
        print("Stopped!")

if __name__ == '__main__':
    main()
