# VPN_Manager
> 机场订阅管理

## Telegram Bot
python-telegram-bot+webhook+nginx+openssl
### Openssl
`mkdir /etc/nginx/ssl`

`cd /etc/nginx/ssl`

`openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out cert.pem`

**Caution:Make sure you enter the correct FQDN!**

### Nginx

`sudo vim /etc/nginx/sites-available/default`

    server {
    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/private.key;
    location /TOKEN {proxy_pass http://127.0.0.1:5000/TOKEN/;}
    }

`sudo systemctl restart nginx`

## 文件说明

[vpn.py](https://github.com/Gc-Mall/VPN_Manager/blob/main/vpn.py) 相关函数库供项目调用

[v2ray_generator.py](https://github.com/Gc-Mall/VPN_Manager/blob/main/v2ray_generator.py) 生成v2ray配置

`python v2ray_generator.py --help --serial number`

[clash_generator.py](https://github.com/Gc-Mall/VPN_Manager/blob/main/clash_generator.py) 生成yaml配置

`python clash_generator.py --help --serial number  --name 'file_name'`

[gladosinfo_check.py](https://github.com/Gc-Mall/VPN_Manager/blob/main/gladosinfo_check.py) 查看各配置使用情况

[v2ray_converter.py](https://github.com/Gc-Mall/VPN_Manager/blob/main/v2ray_converter.py) 机场v2ray配置重命名

[yaml_converter.py](https://github.com/Gc-Mall/VPN_Manager/blob/main/yaml_converter.py) 机场yaml配置重命名

[bot.py](https://github.com/Gc-Mall/VPN_Manager/blob/main/telegram_bot/bot.py) Telegram Bot程序

[checkin.py](https://github.com/Gc-Mall/VPN_Manager/blob/main/checkin.py) 自动签到
