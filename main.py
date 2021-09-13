import urllib3

class findAction():
    def __init__(self, url):
        self.url = url

    def execution():
        # 创建http连接池
        http = urllib3.PoolManager()

        # 抓取一级目录列表
        try:
            response = http.request('GET', url)
        except BaseException as err:
            print(err)
            return None
        # 获取状态码，如果是200表示获取成功
        code = response.status


url = "http://www.chisa.edu.cn"
result = findAction(url)
result.execution()




