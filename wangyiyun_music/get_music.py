#coding:utf-8
import urllib
import urllib2
import re
import cookielib
import json
from bs4 import BeautifulSoup

def get_musicId(url):
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Host':'music.163.com',
              'Referer':'http://music.163.com/',
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    request = urllib2.Request(url,headers=headers)
    html = urllib2.urlopen(request,timeout=10).read()
    html = str(html)
    soup = BeautifulSoup(html)
    plays = soup.find('ul',{'class':'f-hide'})
    title = soup.find('title').string.strip(' -  网易云音乐')
    musicIds = []
    musicNames = []
    for list in plays.findAll('a'):
        href = list.get('href')
        regex = re.compile('\d+')
        musicIds.append(re.search(regex, href).group(0))
        musicNames.append(list.string)
    return musicIds,musicNames,title

def get_music(url):
    musicIds,musicNames,title = get_musicId(url)
    music_hrefs = []
    for musicId in musicIds:
        url = 'http://music.163.com/api/song/detail/?id=%s&ids=[%s]' % (musicId,musicId)
        request = urllib2.Request(url)
        html = urllib2.urlopen(request,timeout=10).read()
        html = str(html)
        regex = re.compile('http://m2.music.126.net/.*?.mp3')
        music_href = re.search(regex, html)
        music_hrefs.append(music_href.group(0))
    return music_hrefs,musicNames,title
        