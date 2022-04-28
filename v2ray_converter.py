import base64
from operator import length_hint
import os
import json
import re
import string
import requests

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

#修改url进行操作
v2ray = V2ray('https://update.glados-config.com/v2ray/155106/e26a4972d833bd82')
addon = ['ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTozNzE4MGM1YWJhZDY5ODcy@46d1f96.sc.gladns.com:8878#Game-JP-01','ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTozNzE4MGM1YWJhZDY5ODcy@46d1f96.sd.gladns.com:8878#Game-JP-02']
v2ray.add(addon)
v2ray.vmess()
v2ray.output()