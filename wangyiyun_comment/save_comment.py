#coding:utf-8
import os
import re
def save_comment(comments,musicNames,title):
    regex = '[?|!|/|\\|\|]' #路径中不合法的字符
    title = re.sub(regex, '-', title)
    path = u'D:\\comment\\' + title.decode() + '\\' 
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        for i in range(len(comments)):
            musicNames[i] = re.sub(regex, '-', musicNames[i])
            filename = path.decode() + musicNames[i].decode() + u'.txt'
            fp = open(filename,'w')
            fp.write(comments[i].decode())
            fp.close()
        return True
    except: return False