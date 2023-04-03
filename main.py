#coding=utf-8
import mysql.connector
from mysql57 import execute_database_operation, msg_database_operation
from telethon import TelegramClient, events, errors
from db import utils
import os
import datetime
import re as regex
import asyncio
import json
from urllib.parse import urlparse

import logging
from logging.handlers import RotatingFileHandler

from telethon.tl.types import PeerChannel
from telethon import utils as telethon_utils
from telethon.extensions import html
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
# 配置访问tg服务器的代理

# config.set('Section_1', 'key_1', 'value_2')    # 注意键值是用set()方法
# config.write(open('config.ini', 'w'))    # 一定要写入才生效

connection = mysql.connector.connect(host=config['mysql']['host'], user=config['mysql']['user'], password=config['mysql']['password'], database=config['mysql']['database'])

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.ERROR)
level = config['logger']['level']
logging.getLogger().setLevel(level)

logpath = f"{config['logger']['path']}/keywords.log"

handler = RotatingFileHandler(
    filename=logpath, maxBytes=5*1024*1024, backupCount=200, encoding='utf-8')  # 最大200MB日志
formatter = logging.Formatter(
    fmt='[%(levelname)s][%(name)s][%(asctime)s]-->%(message)s', datefmt='%Y-%m-%d %H:%M')
handler.setFormatter(formatter)
logger = logging.getLogger('log')
logger.setLevel('DEBUG')
logger.addHandler(handler)


all_channels = []


# 在程序的启动阶段将all_channels.json加载到内存中，并将其存储为全局变量
# with open('channels/all_channels.json', 'r', encoding='utf8') as infile:
#     all_channels_data = json.load(infile)
async def chachacha(channel_id):
  with open('channels/all_channels.json', 'r', encoding='utf8') as infile:
    all_channels = json.load(infile)
    for channel in all_channels:
      if channel['channel_id'] == channel_id:
        return channel['channel_name']
      break
    else:
      return None


# Create a database connection


receiver = -1001953656727

account = config['account']
current_path = os.path.join(os.getcwd(), '')
if not os.path.exists('session'):
    os.mkdir('session')


# from telethon.tl.functions.messages import GetDialogsRequest
# from telethon.tl.types import InputPeerEmpty


proxy = {'proxy_type': 'socks5', 'addr': '206.119.81.71', 'port': 1080,
         'username': 'yuanpeiwenvpn', 'password': 'yuanpeiwenvpn..', 'rdns': True}
client = TelegramClient(
    f"{current_path+'/session/'}{account['username']}", account['api_id'], account['api_hash'], proxy=proxy)
client.start(phone=account['phone'])
bot = TelegramClient(f"{current_path+'/session/'}{account['bot_username']}", account['api_id'],
                     account['api_hash'], proxy=proxy).start(bot_token=account['bot_token'])
logger.info(f'Leave  start: 开始启动')


# import csv
# chats = []
# last_date = None
# chunk_size = 200
# groups=[]

# result = client(GetDialogsRequest(
#              offset_date=last_date,
#              offset_id=0,
#              offset_peer=InputPeerEmpty(),
#              limit=chunk_size,
#              hash = 0
#          ))
# chats.extend(result.chats)

# for chat in chats:
#     try:
#         if chat.megagroup== True:
#             groups.append(chat)
#     except:
#         continue

# print('Choose a group to scrape members from:')
# i=0
# for g in groups:
#     print(str(i) + '- ' + g.title)
#     i+=1

# g_index = input("Enter a Number: ")
# target_group=groups[int(g_index)]

# print('Fetching Members...')
# all_participants = []
# all_participants = client.get_participants(target_group, aggressive=True)

# print('Saving In file...')
# with open("members.csv","w",encoding='utf8') as f:
#     writer = csv.writer(f,delimiter=",",lineterminator="\n")
#     writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
#     for user in all_participants:
#         if user.username:
#             username= user.username
#         else:
#             username= ""
#         if user.first_name:
#             first_name= user.first_name
#         else:
#             first_name= ""
#         if user.last_name:
#             last_name= user.last_name
#         else:
#             last_name= ""
#         name= (first_name + ' ' + last_name).strip()
#         writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
# print('Members scraped successfully.')

# from telethon import utils
# from telethon import functions

# channel =  client.get_entity(chat.migrated_to)
# full =  client(functions.channels.GetFullChannelRequest(your_channel))
# full_channel = full.full_chat
# # full_channel is a ChannelFull
# print(full_channel.migrated_from_chat_id)

def sprint(string, *args, **kwargs):
    """Safe Print (handle UnicodeEncodeErrors on some terminals)"""
    try:
        print(string, *args, **kwargs)
    except UnicodeEncodeError:
        string = string.encode('utf-8', errors='ignore')\
                       .decode('ascii', errors='ignore')
        print(string, *args, **kwargs)


def print_title(title):
    """Helper function to print titles to the console more nicely"""
    sprint('\n')
    sprint('=={}=='.format('=' * len(title)))
    sprint('= {} ='.format(title))
    sprint('=={}=='.format('=' * len(title)))

channel = {
"🟥🟨🟦🟥Telegram万能搜🟥🟨🟦🟥":1375894952,
"超级搜索🚀TG搜群神器":1586057477,
"🔎中文频道/搜索导航/群组导航":1807931486,
"Telegram中文搜索全能王":1256269160,
"中文频道/群组/机器人分享":1241168082,
"超级搜索/中文搜索/中文导航〖搜索神器〗":1306216350,
"AI🫦搜索":1518842006,
"Hao123导航/TG搜群神器":1693220607,
"TG中文群组导航-搜索引擎-百度频道":1225626099,
"超级索引🚀|中文搜索🚀|导航🚀|群组🚀":1318972052,
"中文搜索🚀|导航🚀|群组🚀":1394200686,
"🔈中文搜索群组/频道-TG机器人分享🔈":1149882637,
"超级搜索🚀-TG神器🚀搜索引擎🚀":1297881397,
"TG电报|中文搜索|中文导航群":1658606832,
"TG搜群神器":1213893401,
"Telegram中文搜索频道群组":1464500381,
"超级索引🚀|中文搜索🚀|导航🚀|群组🚀":1611366091,
"超级索引/中文搜索/中文导航〖搜索神器〗":1288840675,
"电报联盟|中文搜索|中文导航群":1593677410,
"谷歌万能导航中文搜索":1861675479,
"Telegram 中文搜索✈️":1534241187,
"中文搜索🚀|导航🚀|群组🚀":1310939995,
"🔍中文搜索引擎▶️🔥资源库实时更新▶️💥发送关键字搜群▶️快手抖音国漫虎牙斗鱼游戏韩漫白丝黑丝灰丝肉丝高跟性感模特妹子学生制服空姐OL职业街拍捆绑私房写真SM舞蹈开车资源合集视频":1485066737,
"TG-电报搜索全能王-群组频道机器人":1748164730,
"中文频道/群组/机器人分享":1365760812,
"中文导航/中文频道/中文搜索【搜群神器】":1500619218,
"电报中文搜索全能王":1187088309,
"中文搜索导航大全":1777109354,
"电报联盟🚀|中文搜索🚀|导航🚀|群组🚀":1698326439,
"电报联盟🚀中文搜索神器🚀TG搜索🚀":1657667314,
"Telegram 中文社群 🅥":1284494558,
"电报搜索/搜索引擎/电报中文":1330885825,
"十万人电报群组频道搜索":1561455638,
"搜索群组🇨🇳中文搜索":1607801945,
"中文搜索🚀|导航🚀|群组🚀":1599771771,
"电报搜索":1501799774,
"安卓软件█破解VPN群":1390741847,
"TG中文搜索频道-搜索大全":1446625906,
"中文群组/频道大全/So1234🔥":1497178746,
"中文索引🚀|中文搜索🚀|导航🚀|群组🚀":1616900283,
"TG群组导航/群组搜索/TG机器人":1634056308,
"电报中文搜索🔥🔥中文导航总群":1665385531,
"M-Team official chat - Chinese":1051902747,
"TG电报/中文/搜索/群组/导航/索引":1871784550,
"中文搜群🚀|索引🚀|搜索":1344228959,
"中文搜群🚀|搜索🚀|索引":1227885925,
"❤️Telegram群组搜索导航❤️":1422778392,
"飞机找群搜群大全":1503884254,
"超级索引🚀|中文搜索🚀|中文频道🔥【搜索神器】":1753262919,
"搜索导航🚀搜群神器🚀福利导航":1525682483,
"🔎中文频道/搜索导航/群组导航":1238118550,
"TG中文频道大全":1313778035,
"百度搜索/中文导航/最全福利索引":1589504989,
"中文导航/中文搜索/中文频道":1719557124,
"🔎中文搜片|超级索引|中文搜索|":1585878490,
"TG全能导航❤️想搜就搜❤️(广告@damoad)":1176022129,
"中文导航/全能搜索/群组/机器人分享":1722810887,
"搜搜":1762814978,
"TG搜群/中文频道/搜索引擎【电报搜索】":1769256624,
"中文搜索引擎🇨🇳搜索群组":1277226355,
"TG中文搜群/搜频道/搜资源":1250644781,
"电报搜索/中文频道/hao123":1827157453,
"【烟花搜索】电报搜索🚀中文导航🚀谷歌搜索":1632110583,
"超级搜索🚀-TG神器🚀搜索引擎🚀":1166396725,
"🔍 狗狗索引 - 官方群组":1798825161,
"TG中文搜索频道":1748347455,
"TG中文群组频道导航【飞机中国】@feiji":1343238716,
"中文｜搜索｜引擎🩸导航":1515183405,
"ChikoRoko 官方中文群🇨🇳":1675173782,
"超级索引🚀中文搜索神器🚀TG搜索🚀":1350526390,
"电报联盟中文频道/中文搜索【搜群神器】":1723937567,
"超级索引🚀中文搜索神器🚀卓创集团🚀":1692835503,
"TG搜群招聘神器🔥导航群":1426384102,
"飞机资源大全soso搜群":1789671685,
"❥搜索导航❥群组搜索":1684542595,
"中文搜索/中文频道/机器人分享【搜索神器】":1571289562,
"TG-电报搜索全能王-群组频道机器人":1512184055,
"Telegram 中文搜索✈️":1874489837,
"电报联盟/中文频道/搜索引擎":1258939448,
"📢中文群组搜索|频道导航":1694816327,
"搜索引擎_开云直招:嘉诚":1778778894,
"社工库机器人群":1434592355,
"搜索引擎🔍关键词回复":1693913401,
"中文频道|中文搜索":1897984751,
"搜索导航🚀搜群神器🚀福利导航":1590915208,
"中文搜索 全网 最全资源 群里啥都有 电报最有趣":1320464791
}
# cur = conn.cursor() # 生成游标对象
# sql="SELECT channel_id as channel_id,channel_name as channel_name from channels" # SQL语句
# cur.execute(sql) # 执行SQL语句
# data = cur.fetchall() # 通过fetchall方法获得数据
# if data:
#   print(data)

# cur.close() # 关闭游标
# conn.close() # 关闭连接



# 列表推导式 获取频道实体列表
channel_list = [PeerChannel(channel[channel_name]) for channel_name in channel]
# @client.on(events.NewMessage(pattern=r'(?i).*欢迎'))
# @client.on(events.NewMessage(from_users=channel_list))
# async def handler(event):

#   print(event.stringify())




@client.on(events.MessageEdited)
@client.on(events.NewMessage())
async def on_greeting(event):
    '''Greets someone'''
    if not event.chat:
      logging.error(f'11111111event.chat empty. event: { event }')
      raise events.StopPropagation

    if event.chat.username == account['bot_username']:  # 不监听当前机器人消息
      logger.debug(f'不监听当前机器人消息: { event.chat.username }')
      raise events.StopPropagation

    # 是否拒绝来自其它机器人发在群里的消息
    if 'block_bot_msg' in config and config['config']['block_bot_msg']:
      if hasattr(event.message.sender, 'bot') and event.message.sender.bot:
        logger.debug(f'不监听所有机器人消息: { event.chat.username }')
        raise events.StopPropagation






    if len(event.message.message) < 12:
      # if not event.is_group:# channel 类型
      if True:  # 所有消息类型，支持群组

        message = event.message
        text = message.text
        if message.file and message.file.name:
          text += ' {}'.format(message.file.name)  # 追加上文件名

        # 打印消息
        _title = ''
        if not hasattr(event.chat, 'title'):
          logging.warning(f'找不到标题:')
        else:
            _title = f'event.chat.title:{event.chat.title},'
        user_id = event.message.from_id.user_id

        #channel_name = event.chat.username
        _username =''
        if not hasattr(event.chat, 'username'):
            logger.debug(f'找不到channel_name')
            # group  =  client.get_entity(f'-100{event.chat.id}')
            # print(group)
            # logger.debug(f'group:{group}')


        #logger.debug(f'user_id: {event.message.from_id.user_id}, channel_name: {event.chat.username}, channel_id:{event.chat.id}, chat_title:{event.chat.title[:20]}, msg_id:{event.message.id}, text:{text},\nevent:{event.chat}')
        logger.debug(f'user_id: {event.message.from_id.user_id}, channel_name: {event.chat.username}, channel_id:{event.chat.id}, chat_title:{event.chat.title[:20]}, msg_id:{event.message.id}, text:{text}')
        # if not event.message.chat.id:
        #     logger.debug(f'找不到user_id:event:{event},\neventmsg:{event.message}')

        # channel_name = event.entity.usernames[0].username if not event.entity.username else event.entity.username
        # print(channel_name)
        # 2.方法：直接发送新消息,非转发.但是可以url预览达到效果

        # 查找当前频道的所有订阅
        sql = """ select id user_id, keywords from user_subscribe_list """
        find = utils.db.connect.execute_sql(sql).fetchall()
        #logger.debug(f'all chat_id & keywords:{find}') # 打印当前频道，订阅的用户以及关键字
        if find:
          # 优先返回可预览url
          # event_chat_username = event.chat.username

          # if not event_chat_username:
          #   event_chat_username = f'-100{event.chat.id}'
          #   #print(event_chat_username)

          #   result = execute_database_operation('select', event_chat_username, conn)['channel_name']

          #   channel_nameok = result['channel_name']
          #   #print({channel_nameok})
          #   conn.close()

         # print(channel_nameok)
          channel_url = f'https://t.me/{event.chat.username}/' if event.chat.username else get_channel_url(
              event.chat.username, event.chat_id)

          # chaxunid= f'-100{event.chat.id}'
          # chaxun = chachacha(chaxunid)
          # logger.debug(f'aaaaaaaaaaaaaaaaaaaaaa:{chaxun}')

          #channel_url = f'https://t.me/{event.chat.username}/' if event.chat.username else execute_database_operation('select', f'-100{event.chat.id}', conn)['channel_name']
          #conn.close()

          channel_msg_url = f'{channel_url}{message.id}'

          chat_title = event.chat.username if event.chat.username else event.chat.title
          logger.debug(f'chat_title: {chat_title}')

          #for receiver,keywords,l_id,l_chat_id in find:
          messagedata = []
          for id, keywords in find:
            try:
              #sender = await message.get_sender()
              if is_regex_str(keywords):  # 输入为正则字符串
                regex_match = js_to_py_re(keywords)(text)  # 进行正则匹配 只支持ig两个flag

                if isinstance(regex_match, regex.Match):  # search()结果

                  regex_match = [regex_match.group()]
                  regex_match_str = []  # 显示内容
                  for _ in regex_match:
                    item = ''.join(_) if isinstance(_, tuple) else _
                    if item:
                      regex_match_str.append(item)  # 合并处理掉空格
                  regex_match_str = list(set(regex_match_str))  # 处理重复元素

                  if regex_match_str:  # 默认 findall()结果
                    sender = await message.get_sender()
                    username = sender.username
                    if sender.username is None:
                      

                      if username is None:
                          jieguo = url_user(f'{channel_msg_url}?embed=1&mode=tme')
                          if jieguo:
                            username = jieguo['username']
                          else:
                            username = ''
                    else:
                          username = sender.username    

                    message_str = f'[#FOUND]({channel_msg_url}) **{regex_match_str}** in {chat_title} @{username}'
                    logger.debug(
                        f'111111111111REGEX: 接收者 chat_id:{receiver}, message_str:{message_str}')
                    messagedata.append({
                        "user_id": event.message.from_id.user_id,                      
                        "chat_id": receiver,
                        "msgid": message.id,
                        "channel_id": event.chat.id,
                        "msg_url": channel_msg_url,
                        "chat_title": chat_title,
                        "keywords":keywords,
                        "text": event.message.text,
                        "status": 1,
                        "username": username,
                        "updatetime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })

                    temp_path = os.path.join(os.getcwd(), 'Message')
                    if not os.path.exists(temp_path):
                      os.mkdir(temp_path)
                    json_file_path = os.path.join(
                        temp_path, f'{message.id}.json')
                    with open(json_file_path, 'w', encoding='utf8') as outfile:
                      json.dump(messagedata, outfile, ensure_ascii=False)

                    result = msg_database_operation('insert', messagedata, connection)
                    if result:
                        logger.debug(f'发送信息写入数据库成功')
                    else:
                        logger.debug(f'写入数据库失败!, erro:{result}, messagedata: {messagedata}')
                        connection.close()
                else:
                  logger.debug(f'regex_match empty. regex:{keywords} ,message: t.me/{event.chat.username}/{event.message.id}')
              else:  # 普通模式
                if keywords in text:
                  sender = await message.get_sender()
                  username = sender.username

                  if username is None:
                      jieguo = url_user(f'{channel_msg_url}?embed=1&mode=tme')
                      if jieguo:
                        username = jieguo['username']
                      else:
                        username = ''
                  else:
                        username = sender.username 
                  message_str = f'[#FOUND]({channel_msg_url}) **{keywords}** in {chat_title} @{username}'
                  logger.debug(f'22222222222222REGEX: 接收者 chat_id:{receiver}, message_str:{message_str}, username:{username}')                      
                  messagedata = {
                      "user_id": event.message.from_id.user_id,                      
                      "chat_id": receiver,
                      "msgid": message.id,
                      "channel_id": event.chat.id,
                      "msg_url": channel_msg_url,
                      "chat_title": chat_title,
                      "keywords":keywords,
                      "text": event.message.text,
                      "status": 1,
                      "username": username,
                      "updatetime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                  }
                  temp_path = os.path.join(os.getcwd(), 'Message')
                  if not os.path.exists(temp_path):
                    os.mkdir(temp_path)
                  json_file_path = os.path.join(
                      temp_path, f'{message.id}.json')
                  with open(json_file_path, 'w', encoding='utf8') as outfile:
                    json.dump(messagedata, outfile, ensure_ascii=False)

                  result = msg_database_operation('insert', messagedata, connection)
                  if result:
                    logger.debug(f'发送信息写入数据库成功')
                  else:
                    logger.debug(f'写入数据库失败!, erro:{result}, messagedata: {messagedata}')
                    connection.close()

                  #await bot.send_message(receiver, message_str,link_preview = True,parse_mode = 'markdown')
                  #raise events.StopPropagation
            except errors.rpcerrorlist.UserIsBlockedError as _e:
              # User is blocked (caused by SendMessageRequest)  用户已手动停止bot
              logging.error(f'{_e}')
              logger.error(f'Error:{_e}')
              pass  # 关闭全部订阅
            except ValueError as _e:
              # 用户从未使用bot
              logging.error(f'{_e}')
              logger.error(f'except ValueError:{_e}')
            except AssertionError as _e:              
              logger.error(f'except AssertionError:{_e}')
              raise _e
            except Exception as _e:
              logging.error(f'{_e}')
              logger.error(f'except Exception:{_e}')
        else:
          #logger.debug(f'sql find empty. event.chat.username:{event.chat.username}, find:{find}, sql:{sql}')
          logger.debug(f'sql find {event.chat.username}')


# # ===================
# # 通过ID获取用户信息
# # ===================
# async def get_user_by_id(user_id=None):
#     u = await client.get_input_entity(PeerUser(user_id=user_id))
#     user = await client(GetFullUserRequest(u))

#     logger.debug(f'{sys._getframe().f_code.co_name}: User ID {user_id} has data:\n {user}\n\n')

#     return {
#         'username': user.user.username,
#         'first_name': user.user.first_name,
#         'last_name': user.user.last_name,
#         'is_verified': user.user.verified,
#         'is_bot': user.user.bot,
#         'is_restricted': user.user.restricted,
#         'phone': user.user.phone,
#     }


def js_to_py_re(rx):
  '''
  解析js的正则字符串到python中使用
  只支持ig两个匹配模式
  '''
  query, params = rx[1:].rsplit('/', 1)
  if 'g' in params:
      obj = regex.findall
  else:
      obj = regex.search

  # May need to make flags= smarter, but just an example...
  return lambda L: obj(query, L, flags=regex.I if 'i' in params else 0)


def is_regex_str(string):
  return regex.search(r'^/.*/[a-zA-Z]*?$', string)


# bot相关操作
def parse_url(url):
  """
  解析url信息 
  根据urllib.parse操作 避免它将分号设置为参数的分割符以出现params的问题
  Args:
      url ([type]): [string]
  
  Returns:
      [dict]: [按照个人认为的字段区域名称]  <scheme>://<host>/<uri>?<query>#<fragment>
  """
  if regex.search('^t\.me/', url):
    url = f'http://{url}'

  res = urlparse(url)  # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
  result = {}
  result['scheme'], result['host'], result['uri'], result['_params'], result['query'], result['fragment'] = list(
      res)
  if result['_params'] or ';?' in url:
    result['uri'] += ';'+result['_params']
    del result['_params']
  return result

import requests
from bs4 import BeautifulSoup
import re
def url_user(url):
  # 发送请求获取页面内容
  response = requests.get(url)
  html_content = response.content
  # 使用BeautifulSoup解析页面
  soup = BeautifulSoup(html_content, 'html.parser')

  username =  soup.a.attrs['href'][ soup.a.attrs['href'].rfind('/') + 1:]
  if username == 'widgets':
      username = '未查询到用户名'
  else:
      username =  soup.a.attrs['href'][ soup.a.attrs['href'].rfind('/') + 1:]

  if username:
    keywords = soup.select_one('.tgme_widget_message_text.js-message_text').get_text()
    usertitle = soup.select_one('a.tgme_widget_message_author_name > span').get_text()
    datetime = soup.select_one('time').get('datetime')
    channel_title = soup.select_one('a.tgme_widget_message_owner_name > span').get_text()
    logger.debug(f'获取用户名成功: {url} - {username} - {channel_title} - {keywords} - {usertitle} - {datetime} ')
    return {
      'username':username,      
      'channel_title':channel_title,
      'keywords':keywords,
      'usertitle':usertitle,
      'datetime':datetime
    }
  else:
    return None

def get_channel_url(event_chat_username, event_chat__id):
  """
  获取频道/群组 url
  优先返回chat_id的url

  https://docs.telethon.dev/en/latest/concepts/chats-vs-channels.html#converting-ids

  Args:
      event_chat_username (str): 频道名地址 e.g. tianfutong 
      event_chat__id (str): 频道的非官方id。 e.g. -1001630956637
  """
  # event.is_private 无法判断
  # 判断私有频道
  # is_private = True if not event_chat_username else False
  host = 'https://t.me/'
  url = ''
  if event_chat__id:
    real_id, peer_type = telethon_utils.resolve_id(
        int(event_chat__id))  # 转换为官方真实id
    url = f'{host}c/{real_id}/'
  elif event_chat_username:
    url = f'{host}{event_chat_username}/'
  return url


# 使用说明
@bot.on(events.NewMessage(pattern='/help'))
async def start(event):
  await event.respond('''
操作方法：

 - 添加关键词(点击复制)
  `/add_keyword 关键字1,关键字2`
  支持js正则语法:
  `/add_keyword /[\s\S]*/ig`

 - 删除关键词(点击复制)
  `/del_keyword 关键字1,关键字2`

 - 删除关键词id
  `/del_id 1,2`

 - 删除所有关键词
  /delete_all

 - 查看关键词列表
  /list
  ''')
  raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
  """Send a message when the command /start is issued."""
  # 使用者的telegram ID
  user_id = event.message.chat.id
  # 非公共服务
  if 'private_service' in config and config['private_service']:
    # 只服务指定的用户
    authorized_users_list = config['authorized_users']
    if user_id not in authorized_users_list:
        await event.respond('Opps! I\'m a private bot. 对不起, 这是一个私人专用的Bot')
        raise events.StopPropagation

  find = utils.db.user.get_or_none(chat_id=user_id)
  if not find:
    insert_res = utils.db.user.create(**{
        'chat_id': user_id,
        'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
  else:  # 存在chat_id
    insert_res = True

  if insert_res:
    await event.respond('你好！请输入 /help ，获取使用方法。')
  else:
    await event.respond('Opps! Please try again /start ')

  raise events.StopPropagation


@bot.on(events.NewMessage(pattern='/add_keyword'))
async def add_keyword(event):
  """Send a message when the command /add_keyword is issued."""
  # 检查使用者的telegram ID
  user_id = event.message.chat.id
  find = utils.db.user.get_or_none(chat_id=event.message.chat.id)
  print(find)
  if not find:  # 不存在用户信息
    await event.respond('Failed. Please input /start')
    raise events.StopPropagation

  text = event.message.text
  text = text.replace('，', ',')  # 替换掉中文逗号
  # 确保英文逗号间隔中间都没有空格  如 "https://t.me/xiaobaiup, https://t.me/com9ji"
  text = regex.sub('\s*,\s*', ',', text)
  splitd = [i for i in regex.split('\s+', text) if i]  # 用空元素分割
  if len(splitd) <= 1:
    await event.respond('命令格式 /add_keyword 关键字1,关键字2 \n 支持js正则语法: `/[\s\S]*/ig`')
    raise events.StopPropagation
  elif len(splitd) == 2:
    command, keywords = splitd
    result = add_keywordlist(keywords.split(','),find)
    if isinstance(result, str):
        logging.error('add_keywordlist 错误：'+result)
        await event.respond(result)  # 提示错误消息
        raise events.StopPropagation
    else:
      msg = ''
      for key in result:
        msg += f'{key},'
      if msg:
        msg = '添加成功:\n'+msg
        text, entities = html.parse(msg)  # 解析超大文本 分批次发送 避免输出报错
        for text, entities in telethon_utils.split_text(text, entities):
          await event.respond(text, formatting_entities=entities)
  raise events.StopPropagation


def add_keywordlist(keywords_list,user_di):
  """
  订阅关键字
  """
  result = []
  for keyword in keywords_list:
    keyword = keyword.strip()
    find = utils.db.user_subscribe_list.get_or_none(**{
        'keywords': keyword,
    })
    if find:
      result.append((keyword))
    else:
      insert_res = utils.db.user_subscribe_list.create(**{
          #'id': '',
          'user_id':user_di,
          'keywords': keyword,
          'channel_name': '',
          'create_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
          'chat_id': ''
      })
      if insert_res:
        result.append((keyword))
  return result


@bot.on(events.NewMessage(pattern='/del_keyword'))
async def del_keyword(event):
  """Send a message when the command /del_keyword is issued."""
  # 检查使用者的telegram ID
  find = utils.db.user.get_or_none(chat_id=event.message.chat.id)
  if not find:  # 不存在用户信息
    await event.respond('Failed. Please input /start')
    raise events.StopPropagation

  text = event.message.text
  text = text.replace('，', ',')  # 替换掉中文逗号
  # 确保英文逗号间隔中间都没有空格  如 "https://t.me/xiaobaiup, https://t.me/com9ji"
  text = regex.sub('\s*,\s*', ',', text)
  splitd = [i for i in regex.split('\s+', text) if i]  # 删除空元素
  if len(splitd) <= 1:
    await event.respond('命令格式 /del_keyword 关键字1,关键字2')
    raise events.StopPropagation
  elif len(splitd) == 2:
    command, keywords = splitd
    result = del_keywordlist(keywords.split(','))
    if isinstance(result, str):
        logging.error('add_keywordlist 错误：'+result)
        await event.respond(result)  # 提示错误消息
        raise events.StopPropagation
    else:
      msg = ''
      for key in result:
        msg += f'{key},'
      if msg:
        msg = '删除关键词成功:\n'+msg
        text, entities = html.parse(msg)  # 解析超大文本 分批次发送 避免输出报错
        for text, entities in telethon_utils.split_text(text, entities):
          await event.respond(text, formatting_entities=entities)
  raise events.StopPropagation


def del_keywordlist(keywords_list):
  """
  取消订阅关键字
  """
  result = []
  for keyword in keywords_list:
    keyword = keyword.strip()
    isdel = utils.db.user_subscribe_list.delete().where(
        utils.User_subscribe_list.keywords == keyword).execute()
    if isdel:
      result.append((keyword))
  return result


@bot.on(events.NewMessage(pattern='/del_id'))
async def del_id(event):
  '''
  根据id取消关键字订阅
  '''
  # 检查使用者的telegram ID
  find = utils.db.user.get_or_none(chat_id=event.message.chat.id)
  if not find:  # 不存在用户信息
    await event.respond('Failed. Please input /start')
    raise events.StopPropagation

  text = event.message.text
  text = text.replace('，', ',')  # 替换掉中文逗号
  # 确保英文逗号间隔中间都没有空格  如 "https://t.me/xiaobaiup, https://t.me/com9ji"
  text = regex.sub('\s*,\s*', ',', text)
  splitd = [i for i in regex.split('\s+', text) if i]  # 删除空元素
  if len(splitd) <= 1:
    await event.respond('命令格式 /del_id 关键字ID1,关键字ID2')
    raise events.StopPropagation
  elif len(splitd) == 2:
    command, keywordids = splitd
    result = del_keywordidlist(keywordids.split(','))
    if isinstance(result, str):
        logging.error('add_keywordlist 错误：'+result)
        await event.respond(result)  # 提示错误消息
        raise events.StopPropagation
    else:
      msg = ''
      for key in result:
        msg += f'{key},'
      if msg:
        msg = '删除关键词成功:\n'+msg
        text, entities = html.parse(msg)  # 解析超大文本 分批次发送 避免输出报错
        for text, entities in telethon_utils.split_text(text, entities):
          await event.respond(text, formatting_entities=entities)
  raise events.StopPropagation


def del_keywordidlist(keywords_idlist):
  """
  取消订阅关键字
  """
  result = []
  for keywordid in keywords_idlist:
    keywordid = keywordid.strip()
    find = utils.db.connect.execute_sql(
        'select id,keywords from user_subscribe_list where id = %s' % (keywordid)).fetchall()
    if find:
      for id, keywords in find:
        isdel = utils.db.user_subscribe_list.delete().where(
            utils.User_subscribe_list.id == id).execute()
        if isdel:
          result.append((keywords))
          logger.debug('del_keywordidlist 成功：' + keywordid)
    else:
      logging.error('del_keywordidlist 错误：' + keywordid + 'not found')
  return result








# 查询当前所有订阅
@bot.on(events.NewMessage(pattern='/list'))
async def _list(event):
  # 检查使用者的telegram ID
  chat_id = event.message.chat.id
  find = utils.db.user.get_or_none(**{'chat_id':chat_id,})
  #find = utils.db.user.get_or_none(chat_id=event.message.chat.id)
# if find:
#   find = utils.db.connect.execute_sql('select id,keywords,channel_name,chat_id from user_subscribe_list where user_id = %d and status  = %d' % (find.id,0) ).fetchall() 
  print(find) 
  if not find:  # 不存在用户信息
    await event.respond('你想干什么？')
    raise events.StopPropagation

  find = utils.db.connect.execute_sql(
      'select id,keywords chat_id from user_subscribe_list where user_id = %d and status  = %d' % (find.id,0) ).fetchall()
  if find:
    msg = ''
    for id, keywords in find:
      msg += f'{id}, {keywords}\n'
    text, entities = html.parse(msg)  # 解析超大文本 分批次发送 避免输出报错
    for text, entities in telethon_utils.split_text(text, entities):
      # await client.send_message(chat, text, formatting_entities=entities)
      await event.respond(text, formatting_entities=entities)
  else:
    await event.respond('没有列表')
  raise events.StopPropagation

# 机器人命令测试

@bot.on(events.NewMessage(pattern='/delete_all'))
async def delete_all(event):
  """Send a message when the command /delete_all is issued."""
  # 检查使用者的telegram ID
  find = utils.db.user.get_or_none(chat_id=event.message.chat.id)
  if not find:  # 不存在用户信息
    await event.respond('你想干什么？')
    raise events.StopPropagation
  user_id = find.id
  #DELETE FROM "main"."user_subscribe_list" WHERE rowid = 4
  # isdel = utils.db.user_subscribe_list.delete().execute()
  # await event.respond('所有关键词删除成功')
  # raise events.StopPropagation

  # 查找当前的订阅数据
  _user_subscribe_list = utils.db.connect.execute_sql('select keywords,channel_name,chat_id from user_subscribe_list where user_id = %d and status  = %d' % (user_id,0) ).fetchall()
  if _user_subscribe_list:
    msg = ''
    for keywords,channel_name,chat_id in _user_subscribe_list:
      channel_url = get_channel_url(channel_name,chat_id)
      msg += 'keyword: {}\nchannel: {}\n---\n'.format(keywords,channel_url)

 
    isdel = utils.db.user_subscribe_list.delete().where(utils.User_subscribe_list.user_id == user_id).execute()
    if isdel:
        print(isdel)





@bot.on(events.NewMessage(pattern='/updateall_channel'))
async def updateall_channel(event):
  # chat_id = event.message.chat.id
  # text = event.message.text

  # #await get_all_channels()
  # await chachacha(text)
  # await event.respond(f'{chachacha}')

  # await event.respond(f'{event.stringify()}')

  # logger.debug(f'测试消息:{text}-{event}')
  raise events.StopPropagation


#=====================
#获取已加入所有群组信息
#=====================
#
# def get_all_channels(client):
#     # 创建channels文件夹，用于存放每个channel_id的json文件
#     temp_path = os.path.join(os.getcwd(), 'channels')
#     if not os.path.exists(temp_path):
#         os.mkdir(temp_path)



async def get_all_channels(client):
    # 创建channels文件夹，用于存放每个channel_id的json文件
    temp_path = os.path.join(os.getcwd(), 'channels')
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

    # 获取所有channel信息并写入到对应的json文件中
    all_channels = []
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    async with client:
      async for dialog in client.iter_dialogs():
          if dialog.is_channel:
              channel_id = dialog.id
              #channel_title = dialog.title[:25]
              channel_title = dialog.title
              channel_is_megagroup = dialog.entity.megagroup
              channel_is_broadcast = dialog.entity.broadcast
              channel_name = dialog.entity.usernames[0].username if not dialog.entity.username else dialog.entity.username
              channel_count = dialog.entity.participants_count
              channel_is_group = dialog.entity.megagroup
              channel_access_hash = dialog.entity.access_hash
              current_channel = {
                  "channel_id": channel_id,
                  "channel_name": channel_name,
                  "channel_title": channel_title,
                  "channel_is_megagroup": channel_is_megagroup,
                  "channel_is_group": channel_is_group,
                  "channel_is_broadcast": channel_is_broadcast,
                  "channel_count": channel_count,
                  "channel_access_hash": channel_access_hash,
                  "updatetime": timestamp
              }
              # 添加当前channel的信息到列表中
              all_channels.append(current_channel)

              json_file_path = os.path.join(temp_path, f'{channel_id}.json')
              with open(json_file_path, 'w', encoding='utf8') as outfile:
                  json.dump(current_channel, outfile, ensure_ascii=False)
              result = execute_database_operation(
                  'insert', current_channel, connection)

              if result:
                print("执行成功")
              else:
                print("执行失败")

      # 将所有channel的信息写入all_channels.json文件中
      all_channels_file_path = os.path.join(temp_path, 'all_channels.json')
      with open(all_channels_file_path, 'w', encoding='utf8') as outfile:
          json.dump(all_channels, outfile, ensure_ascii=False)
# loop.create_task(get_all_channels())
     
if __name__ == "__main__":
    client.run_until_disconnected()

#client.loop.run_until_complete(get_all_channels(client))
# async def ziding():
#   loop = asyncio.get_running_loop()
#   future = loop.run_in_executor()
#   result = await future
#   return result

# if __name__ == "__main__":
#   client.run_until_disconnected()
#   loop = asyncio.get_all_channels()
#   future = loop.get_all_channels()


# async def main(): 
#   asyncio.create_task(get_all_channels())
#   # loop = asyncio.get_running_loop()
#   # while client.is_connected():
#   #   await asyncio.sleep(1)






# if __name__ == "__main__":
#     client.loop.run_until_complete(get_all_channels(client))
#     client.loop.run_until_disconnected()


# def search_channel(channel_id):
#     # 查询指定channel_id的信息
#     with open('all_channels.json', 'r', encoding='utf8') as infile:
#         all_channels = json.load(infile)
#         for channel in all_channels:
#             if channel['channel_id'] == channel_id:
#                 print(channel)
#                 break
#         else:
#             print(f"Channel with ID {channel_id} not found.")


#from mysql57 import execute_database_operation


# Insert data into the channels table
# channel_data = {
#     "channel_id": -1001171111111,
#     "channel_name": "sousuo_souqun",
#     "channel_title": "测试2",
#     "channel_is_megagroup": True,
#     "channel_is_group": True,
#     "channel_is_broadcast": False,
#     "channel_count": 52548,
#     "channel_access_hash": 9076021692457279067,
#     "updatetime": "2023-03-27 02:51:27"
# }
# result = execute_database_operation('insert', channel_data)
# if result:
#     print("Insert successful")
# else:
#     print("Insert failed")

# # Select data from the channels table
#result = execute_database_operation('select', -1001176022129)
#print(result)


# import mysql.connector
# from mysql57 import execute_database_operation,msg_database_operation

# # Create a database connection
# conn = mysql.connector.connect(host="172.25.53.22",user="root",password="root",database="cscscs1")

# # Insert data into the channels table
# channel_data = {
#     "channel_id": -100117222222,
#     "channel_name": "sousuo_souqun",
#     "channel_title": "测试3",
#     "channel_is_megagroup": True,
#     "channel_is_group": True,
#     "channel_is_broadcast": False,
#     "channel_count": 52548,
#     "channel_access_hash": 9076021692457279067,
#     "updatetime": "2023-03-27 02:51:27"
# }
# result = execute_database_operation('insert', channel_data, conn)
# if result:
#     print("Insert successful")
# else:
#     print("Insert failed")

# # Select data from the channels table
# channel_id = -1001171111111
# result = execute_database_operation('select', channel_id, conn)
# print(result)

# Close the database connection
# conn.close()


# channel_id = -1001512184055
# result = execute_database_operation('select', channel_id, conn)
# #print(result)
# channel_name = result['channel_name']
# print(channel_name)

# conn.close()


# msgdata = {
#         "chat_id": 1779960306,
#         "msgid": 33808262,
#         "channel_id": 1365760812,
#         "channel_msg_url": "https://t.me/c/1365760812/33808262",
#         "chat_title": "中文频道/群组/机器人分享",
#         "text": "中文",
#         "username": "",
#         "updatetime": "2023-03-27 02:25:50"
#     }

# result = msg_database_operation('insert', msgdata, conn)
# if result:
#     print("Insert successful")
# else:
#     print("Insert failed")
#     conn.close()


# entity = await client.get_entity('username')
# print(entity)
# title = entity.title
# print(entity.stringify())

# # 列表推导式 获取频道实体列表
# channel_list = [PeerChannel(channel[channel_name]) for channel_name in channel]