import urllib3
from xlutils.copy import copy
from bs4 import BeautifulSoup
import datetime
import requests
import threading
import time
import queue as Queue
import sys

count = 0
start = time.time()

class myThread(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                crawler(self.name, self.q)
            except:
                break
        print("Exiting " + self.name)

def crawler(threadName, q):
        global count
        url = q.get(timeout = 2)

        count += 1
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36'
            }

            requests.packages.urllib3.disable_warnings()
            status = requests.get(url, headers=header, timeout=5, verify=False, allow_redirects=False)

        except:
            with open('log.txt', 'a') as f:
                log = '[{}]  {}  status:error\n'.format(datetime.datetime.now(), url)
                f.write(log)
            return

        if status.status_code != 200 and status.status_code != 301 and status.status_code != 302:
            with open('log.txt', 'a') as f:
                log = '[{}]  {}  status:{}\n'.format(datetime.datetime.now(), url, status.status_code)
                f.write(log)

def findAction(url):

    # 创建http连接池
    http = urllib3.PoolManager()

    # 抓取一级目录列表
    try:
        response = http.request('GET', url)
    except BaseException as err:
        # 无法访问时，同时也记录下该位置
        print(err)
        return
    # 获取状态码，如果是200表示获取成功
    code = response.status
    content = response.data.decode()
    html = BeautifulSoup(content, features='html.parser')

    result = set()

    for item in html.find_all('a'):
        link = item.get('href')
        if(link != None):
            if link == '#':
                pass
            elif link == 'javascript:void(0)':
                pass
            elif link.find('javascript:') != -1:
                pass
            elif link == '/':
                pass
            else:
                if(link.find('http') == -1):
                    link = 'http://www.chisa.edu.cn/'+link
                result.add(link)
    return result

# main
rootUrl = "http://www.chisa.edu.cn"
urlList = findAction(rootUrl)
print(len(urlList))

# 创建5个线程名
threadList = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10']

# 设置队列长度，此行为无限长度
workQueue = Queue.Queue(300)

# 线程池
threads = []

# 创建新线程
for tName in threadList:
    thread = myThread(tName, workQueue)
    thread.start()
    threads.append(thread)


# 将url填充到队列
for url in urlList:
    workQueue.put(url)

#等待所有线程完成
for t in threads:
    t.join()

end = time.time()
print('总时间为：',end-start)
print(count)