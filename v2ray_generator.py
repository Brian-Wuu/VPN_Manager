import base64
from operator import length_hint
import os
import json
import re
import string
import requests

User = []
User.append({'cookie':'_ga=GA1.2.1529817620.1651127721; _gid=GA1.2.1719891254.1651127721; koa:sess=eyJ1c2VySWQiOjkzNzM4LCJfZXhwaXJlIjoxNjc3MDQ3ODAzOTc3LCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=tUtL6OPRGnxiZnpfB-8C4h-Cy7A; _gat_gtag_UA_104464600_2=1',
           'traffic':'',
           'day':'',
           'name':'pro0',
           'email':'2019152327@hrbmu.edu.cn'})
User.append({'cookie':'_ga=GA1.2.1568168250.1651127935; _gid=GA1.2.1519080339.1651127935; koa:sess=eyJ1c2VySWQiOjE1NTEwNiwiX2V4cGlyZSI6MTY3NzA0ODAwNjg4MywiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=BqeiFDAEHMEV3z4MwgURI5y6vH0; _gat_gtag_UA_104464600_2=1',
           'traffic':'',
           'day':'',
           'name':'pro1',
           'email':'2019152312@hrbmu.edu.cn'})
User.append({'cookie':'_ga=GA1.2.772916791.1651128146; _gid=GA1.2.1615665125.1651128146; koa:sess=eyJ1c2VySWQiOjEwMTE5NiwiX2V4cGlyZSI6MTY3NzA0ODIyNzI5MiwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=ebyfWPA1Kl2gT2R7xA63edJzftI; _gat_gtag_UA_104464600_2=1',
           'traffic':'',
           'day':'',
           'name':'pro2',
           'email':'2017158004@hrbmu.edu.cn'})

get_url = 'https://glados.rocks/api/user/status'
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Cookie': ''
}

def get_profile_url(selector) -> dict:
    #通过解析status分析出下载url
    session = requests.session()
    headers['Cookie'] = User[selector]['cookie']
    login_page = session.get(get_url, headers=headers)
    #json():返回类型为字典，可以通过键名来获取响应的值
    r_json = login_page.json()
    return r_json

def download_profile(url) -> string:
    #下载文件
    r = requests.get(url)
    return r.text

def rename(target) -> string:
    #匹配名字分类进行重命名
    if re.search('GLaDOS-N2',target):
        target = re.sub('GLaDOS-N2','Speed',target)
    if re.search('GLaDOS-D1',target):
        target = re.sub('GLaDOS-D1','Pluse',target)
    elif re.search('GLaDOS-Portalgun',target):
        target = re.sub('GLaDOS-Portalgun','Mini',target)
    elif re.search('GLaDOS-GEOIP-',target):
        target = re.sub('GLaDOS-GEOIP-','',target)
    elif re.search('Netflix',target):
        target = re.sub('GLaDOS','',target) 
        target = re.sub('-Netflix','',target) 
        target = 'Netflix' + target
    return target


def parseVmess(vmesslink) -> dict:
    #将vmess url解密
    if vmesslink.startswith('vmess://'):
        bs = vmesslink[len('vmess://'):]
        #paddings
        blen = len(bs)
        bs += "=" * (4 - blen % 4)
        vms = base64.b64decode(bs).decode()
        return json.loads(vms) #转化为dict

class V2ray():
    def __init__(self,url) -> None:
        #下载配置并进行b64解密，decode()将binary转化为str，splitlines()转化为ilist
        data = download_profile(url)
        self.link = base64.b64decode(data).decode().splitlines()
        
    def add(self,addon) -> None:
        #添加节点
        for i in range(len(addon)):
            self.link.append(addon[i])
    
    def vmess(self) -> None:
        vmess_links = []
        vmess_index = []
        for i in range(len(self.link)):
            if self.link[i].startswith('vmess'):
                #若vmess订阅，存在vmess_links，方便进行处理
                vmess_links.append(self.link[i])
                #记录vmess订阅位置，存在vmess_index，方便复原
                vmess_index.append(i)
            elif re.findall('(?<=#).*$',self.link[i]):
                 #重命名非vmess订阅
                name = ''.join(re.findall('(?<=#).*$',self.link[i]))
                self.link[i] = re.sub('(?<=#).*$',rename(name),self.link[i])
        for i in range(len(vmess_links)):
            vms = parseVmess(vmess_links[i])
            vms['ps'] = rename(vms['ps'])
            vmess_links[i] = base64.b64encode(json.dumps(vms).encode())
            vmess_links[i] = 'vmess://' + vmess_links[i].decode()
        for i in range(len(vmess_index)):
            self.link[vmess_index[i]] = vmess_links[i]
        for i in range(len(self.link)):
             self.link[i] = self.link[i] + '\n'
             #添加换行符帮助quantumultx识别服务器

    def output(self) -> None:
        m = ''.join(self.link).encode()
        #‘\n’.join()无法实现换行，需在list元素添加换行符来实现换行
        current_path = os.path.abspath(".")
        file = open('v2ray', 'w', encoding="utf-8")
        data = file.write(base64.b64encode(m).decode())
        file.close()

status =  get_profile_url(1)
profile_url = 'https://update.glados-config.com/v2ray/' + str(status['data']['userId']) + '/' + status['data']['hashed']
print(profile_url)
v2ray = V2ray(profile_url)
addon = ['ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTozNzE4MGM1YWJhZDY5ODcy@46d1f96.sc.gladns.com:8878#Game-JP-01','ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTozNzE4MGM1YWJhZDY5ODcy@46d1f96.sd.gladns.com:8878#Game-JP-02']
v2ray.add(addon)
v2ray.vmess()
v2ray.output()