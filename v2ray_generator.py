import base64
import os
import json
import re
import string
import argparse
import vpn

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
        data = vpn.download_profile(url)
        self.url = url
        self.link = base64.b64decode(data).decode().splitlines()
        
    def add(self) -> None:
        #添加Game节点
        addon_url = self.url
        #替换成netch节点
        addon_url = re.sub('v2ray','netch',addon_url)
        data = vpn.download_profile(addon_url)
        link = base64.b64decode(data).decode().splitlines()
        addon = []
        for i in range(len(link)):
            if re.search('Game',link[i],re.IGNORECASE):
                #筛选Game节点，并换名
                #特别注意re.search，re.fiddal的类型，若要为匹配的字符串，我们可以使用group(num) 或 groups() 匹配对象函数来获取匹配表达式
                name = re.search('(?<=#).*$',link[i]).group(0)
                #选中#后的名称
                newname = 'Game-JP-' + re.search('\d+\.?\d*',name).group(0)
                #'\d+\.?\d*'匹配数字
                link[i] = re.sub(name,newname,link[i])
                addon.append(link[i])
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
                self.link[i] = re.sub('(?<=#).*$',vpn.rename(name),self.link[i])
        for i in range(len(vmess_links)):
            vms = parseVmess(vmess_links[i])
            vms['ps'] = vpn.rename(vms['ps'])
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

def get_parser():
    #命令行传入参数
    parser = argparse.ArgumentParser(description='Generate V2ray For IOS')
    parser.add_argument('--serial', '-s', help='serial 属性，必要参数，选择需要生成的配置序号',type = int,required=True)
    #required=True，必要参数
    return parser

"""
parser = get_parser()
args = parser.parse_args()

if __name__ == '__main__':
    #try exception处理异常情况
    try:
        User = vpn.account_info()
        status =  vpn.get_profile_url(args.serial,User)
        profile_url = 'https://update.glados-config.com/v2ray/' + str(status['data']['userId']) + '/' + status['data']['hashed']
        v2ray = V2ray(profile_url)
        v2ray.add()
        v2ray.vmess()
        v2ray.output()
    except Exception as e:
        print(e)
"""