'''相关函数以供项目调用'''
import requests
import json
import re
import yaml

class Account():
    def __init__(self) -> None:
        User = []
        User.append({'cookie':'_ga=GA1.2.1529817620.1651127721; _gid=GA1.2.1719891254.1651127721; koa:sess=eyJ1c2VySWQiOjkzNzM4LCJfZXhwaXJlIjoxNjc3MDQ3ODAzOTc3LCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=tUtL6OPRGnxiZnpfB-8C4h-Cy7A; _gat_gtag_UA_104464600_2=1',
                     'traffic':'',
                     'day':'',
                     'name':'Pro0',
                     'email':'2019152327@hrbmu.edu.cn'})
        User.append({'cookie':'_ga=GA1.2.1568168250.1651127935; _gid=GA1.2.1519080339.1651127935; koa:sess=eyJ1c2VySWQiOjE1NTEwNiwiX2V4cGlyZSI6MTY3NzA0ODAwNjg4MywiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=BqeiFDAEHMEV3z4MwgURI5y6vH0; _gat_gtag_UA_104464600_2=1',
                     'traffic':'',
                     'day':'',
                     'name':'Pro1',
                     'email':'2019152312@hrbmu.edu.cn'})
        User.append({'cookie':'_ga=GA1.2.772916791.1651128146; _gid=GA1.2.1615665125.1651128146; koa:sess=eyJ1c2VySWQiOjEwMTE5NiwiX2V4cGlyZSI6MTY3NzA0ODIyNzI5MiwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=ebyfWPA1Kl2gT2R7xA63edJzftI; _gat_gtag_UA_104464600_2=1',
                     'traffic':'',
                     'day':'',
                     'name':'Pro2',
                     'email':'2017158004@hrbmu.edu.cn'})
        self.info = User

    def account(self) -> list:
        return self.info
    
    def check(self) -> list:
        get_url = 'https://glados.rocks/api/user/status'
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        headers = {'User-Agent': agent,
                   'Cookie': ''
                   }
        for i in range(len(self.info)):
            session = requests.session()
            headers['Cookie'] = self.info[i]['cookie']
            login_page = session.get(get_url, headers=headers)
    #json():返回类型为字典，可以通过键名来获取响应的值
            r_json = login_page.json()
    #返回结果为二维字典
            traffic = r_json['data']['traffic']/(1024*1024*1024)
            day = r_json['data']['leftDays']
    #提取整数部分
            self.info[i]['day'] = day[0:day.rfind('.')]
    #保留两位小数
            self.info[i]['traffic'] = "%.2f" % traffic
        return self.info

def get_profile_url(selector,User) -> dict:
    #通过解析status分析出下载url
    get_url = 'https://glados.rocks/api/user/status'
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    headers = {
        'User-Agent': agent,
        'Cookie': ''
    }
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

def rename(target) -> str:
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