import os
import yaml #pyyaml模块
import re   #正则表达式
import requests
import string
import json
import argparse

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
    
    def output(self,file_name) -> None:
        current_path = os.path.abspath(".")
        file = open(file_name, "w")
        file.write(yaml.dump(self.data))
        file.close()

def get_parser():
    #命令行传入参数
    parser = argparse.ArgumentParser(description='Generate Yaml For Clash')
    parser.add_argument('--serial', '-s', help='serial 属性，选择需要生成的配置序号',type = int,required=True)
    #required=True，必要参数
    parser.add_argument('--name', '-n', help='name 属性, 输入需要生成的配置名字, 默认值格式为pro.yaml',default = 'pro.yaml')
    return parser

parser = get_parser()
args = parser.parse_args()

if __name__ == '__main__':
    try:
        status =  get_profile_url(args.serial)
        profile_url = 'https://update.glados-config.com/clash/' + str(status['data']['userId']) + '/' + status['data']['code'] +'/' + str(status['data']['port']) + '/' + 'glados.yaml'
        profile = Yaml(profile_url)
        profile.rename_proxy('proxies','name')
        profile.rename_policy('proxy-groups','proxies')
        profile.output(args.name)
    except Exception as e:
        print(e)