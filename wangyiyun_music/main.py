#coding:utf-8
from get_music import get_music
from save_music import save_music
if __name__ == '__main__':
    print u'please input the playListID,like 32507038(http://music.163.com/#/song?id=32507038):'
    url = 'http://music.163.com/playlist?id='
    url += raw_input()
    music_hrefs,musicNames,title = get_music(url)
    save_music(music_hrefs,musicNames,title)