import time


class Lrc:
    def __init__(self):
        self.stime = None
        self.etime = None

    def init(self, filename):
        with open(filename, 'r') as f:
            self.text = f.read()
        self.data = {}
        self.li = []
        self.lyric = []
        for i in self.text.split('\n'):
            s = i.split(']')
            s[0] = s[0][1:]
            if s[0].split(':')[0].isdigit() and s[1] != '':
                self.data[str(round(float(s[0].split(':')[0])*60 + float(s[0].split(':')[1]), 2))] = s[1]
                self.li.append({'time': float(round(float(s[0].split(':')[0])*60 + float(s[0].split(':')[1]), 2)), 'lrc': s[1]})
                self.lyric.append(s[1])
        # print(self.li)
        self.stime = None

    def start(self):
        if self.data == {}:
            return 'Init Error'
        self.stime = time.perf_counter()
        return 'Success'

    def end(self):
        self.data = {}
        self.li = []
        self.stime = None

    def get_point_int(self):
        if self.stime == None:
            return 'Start first'
        # 直接遍历好像也可以吧。。不在乎速度了。
        self.etime = time.perf_counter()
        delta = self.etime - self.stime
        for i in range(0, len(self.li)-1):
            if self.li[i]['time'] <= delta < self.li[i + 1]['time']:
                return i
        if delta >= self.li[len(self.li)-1]['time']:
            self.end()
            return len(self.li)

    def get_point(self):
        if self.stime == None:
            return 'Start first'
        return self.li[self.get_point_int()]['lrc']

    def upper(self, num):
        if num > 0:
            return num
        return 0

    def maxer(self, num, limit):
        if num < limit:
            return num
        return limit

    def get_points(self, height=10):
        if self.stime == None:
            return 'Start first'
        point = int(self.get_point_int())
        top = height / 2
        res = []
        '''
        top = int(self.upper(point-top))
        res = []
        for i in self.lyric[int(top):int(point)]:
            res.append(i)
        for i in self.lyric[int(point):]:
            res.append(i)
        return res
        '''
        if point < height/2:
            for i in range(0, int(height/2)-point):
                res.append('')
            for i in self.lyric:
                res.append(i)
            return res
        else:
            for i in self.lyric[int(point)-int(height/2):]:
                res.append(i)
            return res


if __name__ == '__main__':
    lrc = Lrc()
    lrc.init('Cache\\t.lrc')
    lrc.start()
    last = None
    for i in range(0, 10000):
        time.sleep(0.1)
        lyric = lrc.get_points()
        if last != lyric:
            print(lyric)
            last = lyric

    

