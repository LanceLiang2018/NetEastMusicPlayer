from tkinter import *
from urllib import request
import requests
import urllib
import json
import time
import threading
import pygame
import eyed3
import shutil
import os
from Lrc import Lrc


class Searcher:
    def __init__(self, root):
        self.lable = Label(root, text='搜索歌曲:')
        self.enrty = Entry(root)
        self.button = Button(root, text='搜索', command=self.show_text)
        self.listbox = Listbox(root)
        self.li = []

        self.lable.grid(row=0, column=0)
        self.enrty.grid(row=0, column=1)
        self.button.grid(row=0, column=2)
        self.listbox.grid(row=1, sticky=W + E, columnspan=3)
        self.listbox.bind('<Double-Button-1>', self.listbox_click)

    def show_text(self):
        self.listbox.delete(0, END)
        self.li = []
        key = self.enrty.get()
        if key == '':
            return
        url = 'https://v1.hitokoto.cn/nm/search/%s?type=SONG&offset=0&limit=30' % urllib.parse.quote(key)
        js = requests.get(url).text
        js = json.loads(js)
        if not js['code'] == 200:
            return 'Error code:' + js['code']
        songs = js['result']['songs']
        for song in songs:
            self.li.append(song['id'])
            name = ''
            for artist in song['artists']:
                name = name + artist['name']
                if len(song['artists']) > 1 and artist['name'] != song['artists'][len(song['artists'])-1]['name']:
                    name = name + '、'
            self.listbox.insert(END, name + ' - ' + song['name'])

    def listbox_click(self, event):
        if self.listbox.curselection() == tuple():
            return
        print(self.listbox.get(self.listbox.curselection()))
        print(self.li[self.listbox.curselection()[0]])
        queue.append(["download", [self.li[self.listbox.curselection()[0]]]])
        queue.append(["play", [self.listbox.get(self.listbox.curselection())]])


class Player:
    def __init__(self, root):
        self.lrcdisp = Listbox(root)
        self.button1 = Button(root, text='        <        ', command=self.previous_track)
        self.button2 = Button(root, text='        | |        ', command=self.pause_track)
        self.button3 = Button(root, text='        >        ', command=self.next_track)

        self.lrcdisp.grid(row=0, columnspan=6, sticky=W + E)
        self.button1.grid(row=1, column=0, columnspan=2, sticky=W + E)
        self.button2.grid(row=1, column=2, columnspan=2, sticky=W + E)
        self.button3.grid(row=1, column=4, columnspan=2, sticky=W + E)

    def previous_track(self):
        pass

    def pause_track(self):
        pass

    def next_track(self):
        pass

    def set_lrc(self, lrc):
        self.lrcdisp.delete(0, END)
        for i in lrc:
            self.lrcdisp.insert(END, i)


class Playlist:
    def __init__(self, root):
        self.lable = Label(root, text='播放列表')
        self.listbox = Listbox(root)

        self.lable.grid(row=0)
        self.listbox.grid(row=1)

        self.listbox.bind('<Double-Button-1>', self.play)

    def play(self, event):
        pass


class PlaySound:
    def __init__(self):
        self.lrc = Lrc()

    def download(self, argv):
        print('Try to download:', argv[0])

        ids = argv[0]
        url = 'https://v1.hitokoto.cn/nm/url/%d' % ids
        js = json.loads(requests.get(url).text)

        try:
            file_extension = js['data'][0]['type']
            file_link = js['data'][0]['url']
        except Exception as e:
            print('Get song url error:', e)
            print(js)
            return

        detail_url = 'https://v1.hitokoto.cn/nm/detail/%d' % ids
        detail = json.loads(requests.get(detail_url).text)

        author = ''
        for artist in detail['songs'][0]['ar']:
            author = author + artist['name']
            if len(detail['songs'][0]['ar']) > 1 and artist['name'] != detail['songs'][0]['ar'][len(detail['songs'][0]['ar']) - 1]['name']:
                author = author + '、'

        title = detail['songs'][0]['name']
        lrc_url = 'https://v1.hitokoto.cn/nm/lyric/%d' % ids
        lrc_js = json.loads(requests.get(lrc_url).text)
        lrc = lrc_js['lrc']['lyric']

        if os.path.exists(cachePath + author + ' - ' + title + '.' + file_extension):
            print(author + ' - ' + title + '.' + file_extension, ' exists.')
            return

        print("Download:", author, '-', title + '.' + file_extension)
        global stat
        stat.set("Download: " + author + ' - ' + title + '.' + file_extension)

        try:
            f = open(cachePath + author + ' - ' + title + '.' + file_extension, 'wb')
            f.write(request.urlopen(file_link).read())
            f.close()
            f = open(cachePath + author + ' - ' + title + '.' + 'lrc', 'w')
            f.write(lrc)
            f.close()
        except Exception as e:
            print("Download Error", e)

    def play(self, argv):
        global isPlaying
        global isPausing

        if isPlaying == True:
            self.stop()
            time.sleep(1)
        try:
            eyed3.load(cachePath + 'playing.mp3')
        except Exception as e:
            print('Error when init playing', e)
        isPlaying = True
        try:
            global stat
            stat.set("Play: " + argv[0])
            filename = cachePath + argv[0] + ".mp3"
            print("Try to play:", argv[0] + ".mp3")
            pygame.mixer.music.load('t.wav')
            try:
                print("Delete", cachePath+'playing.mp3')
                os.remove(cachePath + 'playing.mp3')
                print('Delete done.')
            except Exception as e:
                print('Error when deleting:', e)

            print("Copy File:", filename, " -> ", 'playing.mp3')
            shutil.copyfile(filename, cachePath + 'playing.mp3')
            time.sleep(1)
            print('Copy done.')
            filename = cachePath + 'playing.mp3'
            # wait until copy finished

            self.lrc.init(cachePath + argv[0] + ".lrc")

            time_use = eyed3.load(filename).info.time_secs
            track = pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            self.lrc.start()
            # time.sleep(time_use)
            for i in range((time_use+1)*10):
                if not isPlaying:
                    break
                time.sleep(0.1)

            pygame.mixer.music.stop()
            self.lrc.end()
            isPlaying = False

        except Exception as e:
            print("Error when playing.", e)
        print("Finished Playing")

    def stop(self):
        global isPlaying
        isPlaying = False

    def pause(self):
        global isPausing
        global isPlaying
        if not isPlaying:
            return
        pygame.mixer.music.pause()

    def get_lrc(self):
        return self.lrc.get_points()


class Main:
    def __init__(self):
        self.root = Tk()
        self.root.title('Music Player -- Lance Liang')
        self.searcherf = Frame(self.root)
        self.searcherf.grid(row=0, column=0)
        self.playerf = Frame(self.root)
        self.playerf.grid(row=0, column=1)
        self.playlistf = Frame(self.root)
        # self.playlistf.grid(row=0, column=2)

        self.playsound = PlaySound()
        self.searcher = Searcher(self.searcherf)
        self.player = Player(self.playerf)
        self.playlist = Playlist(self.playlistf)

        self.lrc = Lrc()

        t = threading.Thread(target=self.doQueue, args=())
        t.setDaemon(True)
        t.start()

        t = threading.Thread(target=self.lrc_loop, args=())
        t.setDaemon(True)
        t.start()

        pygame.mixer.init()

    def mainloop(self):
        self.root.mainloop()

    def lrc_loop(self):
        last = []
        while True:
            try:
                time.sleep(0.1)
                lrc = self.playsound.get_lrc()
                if len(lrc) == 0 or last == lrc:
                    continue
                last = lrc
                point = self.lrc.get_point_int()
                self.player.set_lrc(lrc)
                self.player.lrcdisp.select_set(5)
            except Exception as e:
                print(e)

    def doQueue(self):
        global queue
        global isPlaying
        while True:
            for do in queue:
                # codes[do[0]](do[1])
                t = threading.Thread(target=codes[do[0]], args=(do[1],))
                t.setDaemon(True)
                t.start()
                if do[1][0] == "play":
                    isPlaying = True
                #threading.Thread.join(t)

            queue = []
            time.sleep(0.1)


queue = []
isPlaying = False
isPausing = False
cachePath = 'Cache/'

main = Main()
stat = StringVar()
stat.set('Hello, Lance.')
status = Label(main.searcherf, textvariable=stat)
status.grid(row=3, column=0, columnspan=2)


def quick_play():
    queue.append(["play", ['许嵩 - 如约而至']])


quickPlay = Button(main.searcherf, text='QuickPlay', command=quick_play)
quickPlay.grid(row=3, column=2)

codes = {
    "download": main.playsound.download,
    "play": main.playsound.play,
    "pause": main.playsound.stop
}

main.mainloop()
