import os
import time
import glob
import aiohttp
import aiofiles
from datetime import datetime, timedelta
from hoshino import Service
from hoshino.typing import CQEvent

api = 'https://api.03c3.cn/api/zb'
module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'imgs')
MAX_KEEP_FILES = 5    # 自动清理旧图片，保留5个文件

def get_today_prefix():
    now = datetime.now()
    cutoff = now.replace(hour=1, minute=15, second=0, microsecond=0)# 为了防止api更新延迟，未过1:15视为前一天
    return (now - timedelta(days=1)).strftime("%Y%m%d") if now < cutoff else now.strftime("%Y%m%d")

def to_uri_path(path):
    return path.replace('\\', '/').replace(" ", "%20") #转换斜杠

def get_latest_image():
    list_of_files = glob.glob(os.path.join(file_path, "today_*.png"))
    return max(list_of_files, key=os.path.getctime) if list_of_files else None

def cleanup_old_images():
    try:
        all_files = sorted(glob.glob(os.path.join(file_path, "today_*.png")), 
                         key=os.path.getctime)
        for old_file in all_files[:-MAX_KEEP_FILES]:
            os.remove(old_file)
            print(f"清理旧文件：{os.path.basename(old_file)}")
    except Exception as e:
        print(f"清理失败：{str(e)}")

async def download_image():
    try:
        os.makedirs(file_path, exist_ok=True)
        date_tag = get_today_prefix()
        filename = f"today_{date_tag}.png"
        final_path = os.path.join(file_path, filename)
        
        if os.path.exists(final_path):
            print("今日新闻已存在，跳过下载")
            return True
            
        async with aiohttp.ClientSession() as session:
            async with session.get(api) as resp:
                if resp.status != 200:
                    print(f"API响应异常：{resp.status}")
                    return False
                
                async with aiofiles.open(final_path, 'wb') as f:
                    await f.write(await resp.read())
                
                print(f"下载成功：{filename}")
                cleanup_old_images()
                return True
                
    except Exception as e:
        print(f"下载失败：{str(e)}")
        if 'final_path' in locals() and os.path.exists(final_path):
            os.remove(final_path)
        return False

sv = Service('今日新闻', enable_on_default=False)

@sv.on_fullmatch(('今日新闻', '每日新闻', '新闻60秒', '新闻60s'))
async def Daily_News(bot, ev: CQEvent):
    if not await download_image():
        await bot.send(ev, '❌获取今日新闻失败，请稍后重试')
        return
    
    if (latest := get_latest_image()):
        await bot.send(ev, f'[CQ:image,file=file:///{to_uri_path(latest)}]')
        time.sleep(2)
        await bot.send(ev, '数据来源:澎湃、人民日报、腾讯新闻、网易新闻、新华网、中国新闻网；每日凌晨1时后更新')
    else:
        await bot.send(ev, '⚠️未找到新闻图片')

@sv.scheduled_job('cron', hour='9', minute='30', jitter=50)
async def autoNews():
    if not await download_image():
        sv.logger.error("定时任务下载失败！")
        return
    
    if (latest := get_latest_image()):
        try:
            await sv.broadcast(f'[CQ:image,file=file:///{to_uri_path(latest)}]')
        except Exception as e:
            sv.logger.error(f"定时推送失败：{str(e)}")
    else:
        sv.logger.error("定时任务未找到最新图片文件")

@sv.on_fullmatch('清理新闻图片') #手动清理
async def manual_clean(bot, ev):
    cleanup_old_images()
    await bot.send(ev, f'已清理，保留最新{MAX_KEEP_FILES}张图片')