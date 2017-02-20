#coding:utf-8
from get_comment import get_comment
from save_comment import save_comment
if __name__ == '__main__':
    print u'please input the playListID,like 32507038(http://music.163.com/#/song?id=32507038):'
    url = 'http://music.163.com/playlist?id='
    url += raw_input()
    comments,musicNames,title = get_comment(url)
    if save_comment(comments,musicNames,title):
        print u'save the hotcomment success!'
    else: 
        print u'save the hotcomment fail!'