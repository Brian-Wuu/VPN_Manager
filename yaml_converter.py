import os
import yaml #pyyaml模块
import re   #正则表达式
import requests
import string

def download_profile(url) -> yaml:
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
    elif re.search('GLaDOS-GEO-',target):
        target = re.sub('GLaDOS-GEO-','',target)
    elif re.search('Netflix',target):
        target = re.sub('GLaDOS','',target) 
        target = re.sub('-Netflix','',target) 
        target = 'Netflix' + target
    return target

class Yaml():
    def __init__(self,url) -> None:
        file_data = download_profile(url)
        # 将yaml转化为字典或列表
        self.data = yaml.load(file_data)

    def rename_proxy(self,key,value) -> None:
        #正则匹配修改服务器名
        for i in range(len(self.data[key])):
            self.data[key][i][value] = rename(self.data[key][i][value])

    def rename_policy(self,key,value) -> None:
        #正则匹配修改服务器名
        for i in range(len(self.data[key])):
            for j in range(len(self.data[key][i][value])):
                self.data[key][i][value][j] = rename(self.data[key][i][value][j])
    
    def output(self) -> None:
        current_path = os.path.abspath(".")
        file = open("Pro3.yaml", "w")
        file.write(yaml.dump(self.data))
        file.close()

#修改url进行操作
profile = Yaml('https://update.glados-config.com/clash/155106/913e482/87853/glados-android.yaml')
profile.rename_proxy('proxies','name')
profile.rename_policy('proxy-groups','proxies')
profile.output()