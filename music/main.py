#coding: utf-8
import urllib2
import re
import os
from bs4 import BeautifulSoup
from time import sleep
def get_music_href(musicId):
    url = 'http://music.163.com/api/song/detail/?id=%s&ids=[%s]' % (musicId,musicId)
    request = urllib2.Request(url)
    html = urllib2.urlopen(request,timeout=10).read()
    html = str(html)
    regex = re.compile('http://m2.music.126.net/.*?.mp3')
    music_href = re.search(regex, html).group(0)
    return music_href

def get_title(musicId):
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Host':'music.163.com',
              'Referer':'http://music.163.com/',
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    url = 'http://music.163.com/song?id=%s' %musicId
    request = urllib2.Request(url,headers=headers)
    html = urllib2.urlopen(request,timeout=10).read()
    html = str(html)
    soup = BeautifulSoup(html)
    title = soup.find('title').string.strip(' -  网易云音乐')
    return title
def download_music(music_href,title,filename):
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Host':'m2.music.126.net',
              'Accept-Encoding':'gzip, deflate, sdch',
              'Accept-Language':'zh-CN,zh;q=0.8',
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    retry = 0
    print u'Download %s from %s' % (title,music_href)
    while retry < 10:
        try:
            request = urllib2.Request(music_href,headers=headers)
            resp = urllib2.urlopen(request,timeout=10)
            music = resp.read()
            fp = open(filename,'wb')
            fp.write(music)
            fp.close()
            break
        except: retry +=1
    if retry < 10: print u'%s Download success!' % title
    else: print u'%s Download failed' % title

def download_save_music(music_href,title):
    path = u'D:\\music\\'
    if not os.path.exists(path):
        os.makedirs(path)
    regex = '[?|!|/|\\|\|]' #路径中不合法的字符
    title = re.sub(regex, '-', title)
    filename = path.decode() + title.decode() + u'.mp3'
    download_music(music_href, title, filename)
    print u'下载结束，地址在D:\\music，程序五秒后自动退出'
    sleep(5)
    
if __name__ == '__main__':
    print u'请输入歌曲的ID： '
    musicId = raw_input()
    music_href = get_music_href(musicId)
    download_save_music(music_href,get_title(musicId))
    