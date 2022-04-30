import os
import yaml #pyyaml模块
import argparse
import vpn

class Yaml():
    def __init__(self,url) -> None:
        file_data = vpn.download_profile(url)
        # 将yaml转化为字典或列表
        self.data = yaml.load(file_data)

    def rename_proxy(self,key,value) -> None:
        #正则匹配修改服务器名
        for i in range(len(self.data[key])):
            self.data[key][i][value] = vpn.rename(self.data[key][i][value])

    def rename_policy(self,key,value) -> None:
        #正则匹配修改服务器名
        for i in range(len(self.data[key])):
            for j in range(len(self.data[key][i][value])):
                self.data[key][i][value][j] = vpn.rename(self.data[key][i][value][j])
    
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
        User = vpn.Account().account()
        status =  vpn.get_profile_url(args.serial,User)
        profile_url = 'https://update.glados-config.com/clash/' + str(status['data']['userId']) + '/' + status['data']['code'] +'/' + str(status['data']['port']) + '/' + 'glados.yaml'
        profile = Yaml(profile_url)
        profile.rename_proxy('proxies','name')
        profile.rename_policy('proxy-groups','proxies')
        profile.output(args.name)
    except Exception as e:
        print(e)