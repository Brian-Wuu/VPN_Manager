import os
import logging
from cmath import inf
from asyncio import Task
from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import vpn
from clash_generator import Yaml
from google_drive import Google_drive
from v2ray_generator import V2ray

PORT = int(os.environ.get('PORT', '5000'))

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def check_command(update: Update, context: CallbackContext) -> None:
    """Check Account Info"""
    info = vpn.Account().check()
    reply_text0 = '账户：' + info[0]['name'] + '\n' + '剩余天数：' + info[0]['day'] + '天' + '\n' + '已用流量：' + info[0]['traffic'] + 'G/500G' + '\n'
    reply_text1 = '账户：' + info[1]['name'] + '\n' + '剩余天数：' + info[1]['day'] + '天' + '\n' + '已用流量：' + info[1]['traffic'] + 'G/500G' + '\n'
    reply_text2 = '账户：' + info[2]['name'] + '\n' + '剩余天数：' + info[2]['day'] + '天' + '\n' + '已用流量：' + info[2]['traffic'] + 'G/500G' + '\n'
    update.message.reply_text(reply_text0+reply_text1+reply_text2)

def generate_command(update: Update, context: CallbackContext) -> None:
    """Generate VPN Profile"""
    User = vpn.Account().account()
    #生成并上传clash配置到相应文件夹
    for i in range(3):
        status =  vpn.get_profile_url(i,User)
        profile_url = 'https://update.glados-config.com/clash/' + str(status['data']['userId']) + '/' + status['data']['code'] +'/' + str(status['data']['port']) + '/' + 'glados.yaml'
        profile = Yaml(profile_url)
        profile.rename_proxy('proxies','name')
        profile.rename_policy('proxy-groups','proxies')
        update_drive_service_name = 'pro' + str(i) + '.yaml'
        profile.output(update_drive_service_name)
        task = Google_drive()
        current_path = os.path.abspath(".")
        current_path = current_path + "/" + update_drive_service_name
        task.update_file(update_drive_service_name, current_path, task.search_file('clash', task.fold[task.fold['fold_name'][i]], is_delete_search_file=False))
        #上传完成后删除本地文件
        current_path = os.path.abspath(".")
        os.remove(update_drive_service_name)
    #生成并上传v2ray配置到相应文件夹
    for i in range(3):
        status =  vpn.get_profile_url(i,User)
        profile_url = 'https://update.glados-config.com/v2ray/' + str(status['data']['userId']) + '/' + status['data']['hashed']
        v2ray = V2ray(profile_url)
        v2ray.add()
        v2ray.vmess()
        v2ray.output()
        update_drive_service_name = 'v2ray'
        task = Google_drive()
        current_path = os.path.abspath(".")
        current_path = current_path + "/" + update_drive_service_name
        task.update_file(update_drive_service_name, current_path, task.search_file('shadowrocket', task.fold[task.fold['fold_name'][i]], is_delete_search_file=False))
        #上传完成后删除本地文件
        current_path = os.path.abspath(".")
        os.remove(update_drive_service_name)
    update.message.reply_text("配置生成成功！")

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5321390481:AAEOrakJa19TqsVzfkv8zBtxM3v7wHsnTSE")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("check", check_command))
    dispatcher.add_handler(CommandHandler("generate", generate_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    #updater.start_polling()
    updater.start_webhook(listen="127.0.0.1",
                      port=PORT,
                      url_path="5321390481:AAEOrakJa19TqsVzfkv8zBtxM3v7wHsnTSE",
                      webhook_url = "https://104.208.73.168/" + "5321390481:AAEOrakJa19TqsVzfkv8zBtxM3v7wHsnTSE",
                      cert='/etc/nginx/ssl/cert.pem')
    updater.idle()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.


if __name__ == '__main__':
    main()
