# -*- coding: utf-8 -*-
import os,stat
import requests
import json
import time
import urllib.request
from hoshino import Service
from hoshino.typing import CQEvent

api = 'https://api.03c3.cn/zb/api.php'
file_path = './hoshino/modules/Daily_News/imgs'
file_me = '60s'

def download_image():
    response = requests.get(api)
    loads = json.loads(response.text)
    image_url = loads.get('imageUrl')
    print('正在下载资源')
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)            
        #下载保存图片
        #file_suffix = os.path.splitext(image_url)[1]
        file_name = '{}{}{}{}'.format(file_path,os.sep,'today','.png') 
        urllib.request.urlretrieve(image_url,filename=file_name) 
        print("Download Successful！")
    except IOError as e:
        print("IOError,Please check on")
    except Exception as e:
        print("Exception")


if __name__ == '__main__':
    download_image()

sv = Service('Daily_News')

@sv.on_fullmatch(('今日新闻','每日新闻','新闻60秒','新闻60s'))
async def Daily_News(bot, ev:CQEvent):
    tdimg = 'today' + ".png" 
    image_path = os.path.join(os.path.dirname(__file__),'imgs/',tdimg)
    print (image_path)
    try:
        download_image()
        await bot.send(ev, f'[CQ:image,file=file:///{image_path}]')
        time.sleep(2)
        await bot.send(ev,'数据来源:澎湃、人民日报、腾讯新闻、网易新闻、新华网、中国新闻网；每日凌晨1时后更新')
    except:
        await bot.send(ev,'获取失败，请重试或联系管理员')
