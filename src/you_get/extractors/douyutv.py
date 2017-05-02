
__all__ = ['douyutv_download']

from ..common import *

import requests
import m3u8
import datetime
from selenium.webdriver import PhantomJS
from selenium import webdriver
from urllib.parse import urlparse
import time
import signal

class SteamURLCrack():

    driverPath = {
        # "PhantomJS":"/Users/baibing/phantomjs-2.1.1-macosx/bin/phantomjs"
        "PhantomJS":
        "D:/Program Files (x86)/phantomjs-2.1.1-windows/bin/phantomjs"
        # "PhantomJS":"/usr/local/bin/phantomjs"
    }

    mobile_user_agents = [
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, "
        "like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.7.1",
        "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; KNT-UL10 Build/HUAWEIKNT-UL10) AppleWebKit/534.30 (KHTML, like Gecko) Version"
        "/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.6.0) WindVane/8.0.0 1080X1806 GCanvas/1.4.2.21",
        "Mozilla/5.0 (iPhone 6sp; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 MQQBrowser"
        "/7.3 Mobile/14E277 Safari/8536.25 MttCustomUA/2 QBWebViewType/1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Mobile/14E277 baiduboxapp"
        "/0_31.1.3.8_enohpi_1002_5211/3.01_2C2%259enohPi/1099a/0539A0BD37CDA78C0BA4F242770B24BDAB6895040FRDNQFLKIH/1",
        "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; SM-G9280 Build/MMB29K) AppleWebKit/534.30 (KHTML, like Gecko) Version/"
        "4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.5.3) WindVane/8.0.0 1440X2560 GCanvas/1.4.2.21",
        "Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; MX5 Build/LMY47I) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser"
        "/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.5.3) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
        "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; OPPO R9 Plustm A Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version"
        "/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.6.0) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21",
        "Mozilla/5.0 (Linux; Android 5.1.1; SM801 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome"
        "/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043024 Safari/537.36 MicroMessenger/6.5.4.1000 NetType/4G Language/zh_CN",
        "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; SM801 Build/LMY47V) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 "
        "UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.5.3) WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21"
    ]

    room_url = ""
    rules = {
        "www.douyu.com": {
            "xpath": "//video/@src",
            "url_prefix": "http://m.douyu.com/"
        }
    }

    def __init__(self, room_url):
        self.room_url = room_url
    


    def get_video_src(self):

        #room url check
        o = urlparse(self.room_url)
        rule_key = o.netloc

        if rule_key in self.rules:
            cap = webdriver.DesiredCapabilities.PHANTOMJS

            cap["phantomjs.page.settings.resourceTimeout"] = 1000
            cap["phantomjs.page.settings.loadImages"] = True
            cap["phantomjs.page.settings.disk-cache"] = True
            cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0(iPhone;CPU iPhone OS 9_1 like Mac OSX) AppleWebKit / 601.1"
            ".46(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
            driver = PhantomJS(
                self.driverPath["PhantomJS"], desired_capabilities=cap)
            # 指定使用的浏览器
            # driver = webdriver.Firefox()
            driver.implicitly_wait(10)
            my_rule = self.rules[rule_key]

            url_prefix = my_rule["url_prefix"]
            driver.get("%s%s" % (url_prefix, o.path))
            try:
                result_video = driver.find_element_by_tag_name(
                    'video').get_attribute('src')
                driver.close()
                return result_video

            except:
                # return "未能获得该直播间地址直播流地址"
                driver.close()
                return "主播不在了"
                # return " "
        else:

            return "不支持的网站(not support url)"
            # return " "


def handler(signum, frame):
    raise AssertionError
def get_name(url):
    room_id=url.split('/')[-1]
    json_request_url = "http://open.douyucdn.cn/api/RoomApi/room/%s" % room_id
    content = get_content(json_request_url)
    data = json.loads(content)['data']
    server_status = data.get('error',0)
    if server_status is not 0:
        raise ValueError("Server returned error:%s" % server_status)
    title = data.get('room_id')
    return title

def douyutv_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    """直播流网址"""
    title=get_name(url)
    file_list=[]
    for i in range(4):
        url_video=SteamURLCrack(url).get_video_src()
        # print("视频流地址已获取到")
        # print(url_video)
        if 'http' in url_video:
            #分析直播流网址将网址转换为.ts 格式
            url_1=url_video.split('playlist')[0]
            data=requests.get(url_video,headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
        })
            data.encoding = "gbk"
            content = data.text
            m3u8_obj=m3u8.loads(content)
            
            for key,value in enumerate(m3u8_obj.files):
                url_=url_1+value.split('?')[0]
                # print('流地址%s'%url_)
                try:
                    signal.signal(signal.SIGTERM, handler)
                    signal.alarm(10)
                    download_url_ffmpeg(url_,title+'%s_%s'%(i,key),'flv',None,output_dir=output_dir,merge=merge)
                    file_list.append(output_dir+'/'+title+'%s_%s'%(i,key)+".flv")
                    signal.alarm(0)
                except AssertionError:
                    pass

        else:
            print("the %s is don't have video"%title)
    for name_1 in file_list:
        if os.path.exists(name_1):
            with open('%s.txt'%title,'a')as f:
                f.write("file "+"\'%s\'"%name_1.split('/')[-1]+"\n")
    flv_file=title+'_'+datetime.datetime.now().strftime('%Y%m%d%H%M')
    if os.path.exists(output_dir+'/'+'%s.txt'%title):
        cmd="ffmpeg -f concat -i %s.txt -c copy %s%s.flv"%(title,output_dir+'/',flv_file)
        os.system(cmd)
    if os.path.exists(output_dir+"/"+"%s.flv"%flv_file):
        for i in file_list:
            os.remove(i)
        os.remove('%s.txt' % title)
site_info="douyu.com"
download=douyutv_download

    





