# 人懒，问就是女生自用

由于本项目重构后部署过于复杂，如果你真的想部署一个irori，建议直接开Issue问，而不是看这个我半年才更新一次的Readme。

![头像](Assets/E2.png)

# bot-irori 

一个命令式，主要支援文字形式信息处理的服务接口。

同时提供mirai-http-api接口和websocket外部应用接口。

## features

### 面向用户

- [x] 每日求签~~算命~~
- [x] 答案之书（不知道为什么群友总能玩出新花样
- [x] 谷歌翻译，百度翻译（fufu提供的爬虫
- [x] ddl事件安排及提醒
- [x] 搜歌
- [x] 表达式即时求值的计算器
- [x] LaTeX公式渲染（其实是爬虫
- [x] CodeForces、AtCoder、牛客、力扣、洛谷的比赛提醒推送
- [x] 搜番
- [x] 每日天气预报

完整功能请部署后使用#h查看

### 面向开发

- [x] 调试友好的远程系统命令调用(eval, exec, os.popen)
- [x] 代码热重载
- [x] 方便、可扩展的命令编写
- [x] 保留消息链实现，支援多媒体信息
- [x] 中心Server，多Worker，消息队列部署任务架构，可胜任计算密集任务并发处理，任务超时自动杀死

## requirements

### MongoDB

安装运行服务启动即可，如需网络访问建议弄个数据库级别的登录认证。

### RabbitMQ

由Celery依赖，部署完毕启动即可。

### Python3.8+

以后可能会引入match语法而需要3.10+

依赖包参见[OS_requirements.txt](OS_requirements.txt)

配置最麻烦的模块是[celery](https://github.com/celery/celery)，还请参见其仓库的指南。

### Mirai 2.0+（QQbot必须）

别忘了装上配套的mirai-http-api插件

## deployment

服务器节点的入口是[Server.py](Server.py), 直接使用`python3 Server.py`即可运行

执行模块节点的入口是[Worker.py](Worker.py), 使用`celery -A Worker worker`运行

### cfg.py配置模板

```python
# 数据库连接认证一条龙串
db = {"host": "mongodb://user:password@localhost:27017/irori_data?authSource=yourauthsource"}
# 百度翻译用的api接口
baidu_appid = "114514"
baidu_secretKey = "1919810"

web_host = '0.0.0.0' # Server监听网卡
web_port = 41919 # Server监听端口
dist_host = 'http://127.0.0.1' # Worker访问Server的地址，注意不要加上尾随/
```

Server和Worker都启动成功后，浏览器访问Server监听的网口，转到/docs路径，用屏幕打印的uuid进行身份验证（用户名和密码都填uuid）

然后若要对接mirai-http-api，在/auth/mirai接口处填入其ws链接

若要使用ws连接，请向/ws发送请求。

（没更完，写累了）

## 系统命令手册

sudo 系列命令只有在消息的发送来源包括在auth_masters内的时候会执行。

有关auth_masters的配置，请在数据库中的irori_config的collection下直接配置。

| 命令 | 描述 |
| ------ | ----- |
| sudo exec | 执行一条python exec语句，获取其stdout |
| sudo eval | 执行一条python语句，并返回结果（由于不支持赋值等无返回值操作，故提供exec） |
| sudo run | 在宿主机上运行一条shell命令 |


## 参与开发

参见[DEV.md](DEV.md)或者本仓库的Wiki

## TODOs:

+ 小坑

+ [ ] 实现生命棋
+ [ ] 实现Fygon计算复杂度
+ [ ] 求二次剩余
+ [ ] 选课
+ [ ] 对接屑站转发抽奖
+ [ ] 自用本校工具箱
+ [ ] 百度TTS和谷歌TTS
+ [ ] 重构CF爬虫
+ [ ] 增加MML合成音频标准

+ 大坑
  
+ [ ] 完善暂时闭源的AVG然后一起开源
+ [ ] ai棋牌
+ [ ] TRPG
+ [x] irori-OpenJudge（但是自建果然不如对接
+ [ ] irori农场（
+ [ ] 文档重构
+ [ ] TG消息同步和推送

+ 卫星

+ [ ] 《奇点》
+ [ ] irori前端面板
+ [ ] 聊天机器人
+ [ ] 形象重绘 ~~机伤网站关了（悲~~
+ [ ] ~~出道~~

## 引用项目:

[Kumbong/quine_mccluskey](https://github.com/Kumbong/quine_mccluskey)

[be5invis/Sarasa-Gothic](https://github.com/be5invis/Sarasa-Gothic)

## 其它引用资源（侵删）

[telegram: 疯狂星期四文案收集姬](https://t.me/crazythu)

## irori的好朋友

[ssttkkl/PixivBot](https://github.com/ssttkkl/PixivBot)

[KutouAkira/bot_fufu](https://github.com/KutouAkira/bot_fufu)

# 妙妙屋沙雕日常

> 不会吧不会吧，不会真的有人什么都问答案之书吧？

![](Assets/kusa/1.png)

![](Assets/kusa/2.jpg)

![](Assets/kusa/3.jpg)

![](Assets/kusa/4.jpg)

![](Assets/kusa/5.jpg)

![](Assets/kusa/6.png)

![](Assets/kusa/7.jpg)

![](Assets/kusa/8.png)

![](Assets/kusa/9.png)

![](Assets/kusa/10.png)

![](Assets/kusa/11.png)

![](Assets/kusa/12.png)

![](Assets/kusa/13.png)

![](Assets/kusa/14.png)

![](Assets/kusa/15.png)

![](Assets/kusa/16.png)

![](Assets/kusa/17.png)

![](Assets/kusa/18.png)

![](Assets/kusa/19.png)

![](Assets/kusa/20.png)

**欢迎投稿（**

# 本项目采用AGPLv3.0协议开源
