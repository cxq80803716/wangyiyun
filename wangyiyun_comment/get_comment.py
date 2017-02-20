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
def get_comment(url):
    musicIds,musicNames,title = get_musicId(url)
    Comments =[]
    for i in range(len(musicIds)):
        id = musicIds[i]
        url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=' % id
        referer = 'http://music.163.com/song?id='+id #原链接
        #获得一个cookieJar实例
        cj = cookielib.CookieJar()
        #cookieJar作为参数，获得一个opener的实例
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        #伪装成一个正常的浏览器，避免有些web服务器拒绝访问。
        opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'),
                             ('Referer',referer)]
        #需要访问数据源Headers中的的url
        #最下面需要提交的数据,以键值对进行储存
        submit_data = urllib.urlencode({'params':'FlqQoLOOSzaCwC4AHFw/PJP4oWocxsD7/RAxTWwrtBRnOSDuN6N2D0XPtOlAVErJncuu3feCtBpsfB42rHCnmDsiygj/xaROFdjKzEXWrQD0zl28TzXcQjFgBON7ZCvR3XeKDuc3gA2wIV3dW/fRmlABg9uUNQMxWxJXzKOFLxHleVO+zzlCKzQSyKSp9/fj',
                                        'encSecKey':'8d26ed3b970e32cba32247789da4f86910a248f5cc2ecb4747729efe7d6e7b704376e286c299a7a6a973f5ff0b8e02abae34524b12c3c80621a6da40a804395ed1a405f95727b0e38c131d8d53414f0cf8f90d4e011a2a15f6ae52e2f597084f72098a22c60ea40240dd6d461a20ba58e6361ac2980284e4c8ed06676b8095b1'})
        #以post的方法访问登陆页面，访问之后cookieJar会自动保存cookie
        op = opener.open(url,submit_data)
        #读取获得的数据源
        data = op.read()
        #解析成json数据,接下来就可以直接以键值对的方式访问数据源了
        data = json.loads(data)
        comment = data['hotComments']
        comments =u'<   ' + musicNames[i] + u'   > : \n'
        count = 1
        for cm in comment:
            comments =comments + str(count) + ': ' + cm['content'] + u"点赞数: " + str(cm['likedCount']) + u'\n'
            count +=1
        if count ==1:  #没有热门评论
            comments += u'No hotcomment!'
        Comments.append(comments)
    return Comments,musicNames,title
        