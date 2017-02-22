#coding:utf-8
import urllib2
import os
import re
from time import sleep
from multiprocessing import Process, Queue, Pool
from _socket import timeout
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Host':'m2.music.126.net',
              'Accept-Encoding':'gzip, deflate, sdch',
              'Accept-Language':'zh-CN,zh;q=0.8',
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def download_music(musicName,music_href,filename):
    retry = 0
    print u'Download %s from %s' % (musicName,music_href)
    while retry < 8:
        try:
            request = urllib2.Request(music_href,headers=headers)
            resp = urllib2.urlopen(request,timeout=10)
            music = resp.read()
            fp = open(filename,'wb')
            fp.write(music)
            fp.close()
            break
        except: retry +=1
    if retry < 8: print u'%s Download success!' % musicName
    else: print u'%s Download failed' % musicName
    
def save_music(music_hrefs,musicNames,title):
    regex = '[?|!|/|\\|\|]' #路径中不合法的字符
    title = re.sub(regex, '-', title)
    path = u'D:\\music\\' + title.decode() + '\\' 
    if not os.path.exists(path):
        os.makedirs(path)
    pool = Pool(10)
    for i in range(len(music_hrefs)):
        musicNames[i] = re.sub(regex, '-', musicNames[i])
        filename = path.decode() + musicNames[i].decode() + u'.mp3'
        pool.apply_async(download_music,(musicNames[i], music_hrefs[i], filename))
    pool.close()
    pool.join()
    print u'下载结束，地址在D:\\music，程序五秒后自动退出'
    sleep(5)