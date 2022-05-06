import schedule
import time
import vpn

schedule.every().day.at("23:30").do(vpn.Account().checkin)         # 每天在 10:30 时间点运行 job 函数
while True:
    schedule.run_pending()   # 运行所有可以运行的任务
    time.sleep(1)