from tkinter import *
from bs4 import BeautifulSoup as bs
from urllib import request
import json

SaveDir = 'songs/'


def getSong(url):
    js_ = request.urlopen(url).read()
    js = json.loads(js_)

    author = js['songinfo']['author']
    title = js['songinfo']['title']
    lrclink = js['songinfo']['lrclink']
    pic = js['songinfo']['pic_radio']
    album_title = js['songinfo']['album_title']
    file_extension = js['bitrate']['file_extension']
    file_link = js['bitrate']['file_link']

    print("Download:", author, '-', title + '.' + file_extension)

    try:
        f = open(SaveDir + author + ' - ' + title + '.' + file_extension, 'wb+')
        f.write(request.urlopen(file_link).read())
        f.close()
        f = open(SaveDir + author + ' - ' + title + '.' + 'lrc', 'wb+')
        f.write(request.urlopen(lrclink).read())
        f.close()
    except Exception as e:
        print(e)


def searchSong(key):
    url = 'http://music.baidu.com/search?key=' + key
    html = request.urlopen(url).read()
    soup = bs(html, 'html.parser')
    hrefs = soup.find_all('span', attrs={'class': 'song-title'})
    for href in hrefs:
        # print(href.get_text(), end=':\t')
        dat = href.find_all('a')[0].get('data-songdata')
        js2 = json.loads(dat)
        # print(js2['id'])
        getSong('http://musicapi.qianqian.com/v1/restserver/ting?method=baidu.ting.song.play&format=json&songid='
                + js2['id'])


if __name__ == '__main__':
    # key = input('input what you want to search:')
    root = Tk()
    root.title('Music Box -- Lance Liang')
    root.geometry('800x600')
    Label(root, text='搜索').grid(row=0, column=0)
    searchEntry = Entry(root)
    searchEntry.grid(row=0, column=1)
    searchButton = Button(root, text='搜索')
    searchButton.grid(row=0, column=2)
    root.mainloop()
    # searchSong(key)
