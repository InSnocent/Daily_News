# -*- coding: utf-8 -*-
import os
import json
import time
import aiohttp
import aiofiles
from hoshino import Service
from hoshino.typing import CQEvent

api = 'https://api.03c3.cn/api/zb'
file_path = './hoshino/modules/Daily_News/imgs'
file_me = '60s'

async def download_image():
    image_url = api
    print('正在下载资源')
    try:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_name = os.path.join(file_path, 'today.png')
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status == 200:
                    async with aiofiles.open(file_name, 'wb') as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            await f.write(chunk)
                    print("Download Successful！")
                else:
                    print("Failed to download image")
    except Exception as e:
        print("Exception:", str(e))

if __name__ == '__main__':
    import asyncio
    asyncio.run(download_image())

sv = Service('Daily_News', enable_on_default=False)

@sv.on_fullmatch(('今日新闻', '每日新闻', '新闻60秒', '新闻60s'))
async def Daily_News(bot, ev: CQEvent):
    tdimg = 'today' + ".png"
    image_path = os.path.join(os.path.dirname(__file__), 'imgs/', tdimg)
    print(image_path)
    try:
        await download_image()
        await bot.send(ev, f'[CQ:image,file=file:///{image_path}]')
        time.sleep(2)
        await bot.send(ev, '数据来源:澎湃、人民日报、腾讯新闻、网易新闻、新华网、中国新闻网；每日凌晨1时后更新')
    except:
        await bot.send(ev, '获取失败，请重试或联系管理员')

@sv.scheduled_job('cron', hour='09', minute='30', jitter=50)
async def autoNews():
    tdimg = 'today' + ".png"
    image_path = os.path.join(os.path.dirname(__file__), 'imgs/', tdimg)
    await download_image()
    await sv.broadcast(f'[CQ:image,file=file:///{image_path}]')
