# Daily_News
这是一个基于HoshinoBot的每日新闻插件
## 使用方法
1.clone本插件：
在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目
````
git clone https://github.com/InSnocent/Daily_News.git
````

2.依赖：
````
pip install -r requirements.txt
````

3.启用模块

在 HoshinoBot\hoshino\config\bot.py 文件的 MODULES_ON 加入 'Daily_News'

然后重启 HoshinoBot

触发关键词：'今日新闻','每日新闻','新闻60秒','新闻60s'

## 其他
**注：本插件使用的API于每日凌晨一点更新，请于这个点后使用**

**数据来源:** 澎湃、人民日报、腾讯新闻、网易新闻、新华网、中国新闻网；
