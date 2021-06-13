# 人懒，问就是女生自用

# bot-irori 

irori是一个比较扭曲的，偏面向过程的，支持二次开发的QQ机器人

底层协议依赖mirai，并使用graia框架

release里可以找到即拆即用的mirai环境包

## features

+ git更新即时重载
+ 允许多重存在，并支持多实例管理
+ 聊天窗口进行系统命令调用或开shell
+ 插件化的消息处理业务代码管理
+ 三种模式处理消息：命令，监听器，定时订阅
+ 返回消息多态化：可以选择粘贴至ubuntu pastebin，渲染为图片，或者合成为语音

## 比较受欢迎的功能

+ [x] 每日求签~~算命~~
+ [x] 答案之书（不知道为什么群友总能玩出新花样
+ [x] 谷歌翻译，百度翻译（fufu提供的爬虫
+ [x] ddl事件安排及提醒
+ [x] 表达式即时求值的计算器
+ [x] LaTeX公式渲染（其实是爬虫
+ [x] CodeForces、AtCoder、牛客的比赛提醒推送

完整功能请部署后使用#h查看

## 前置知识

本篇README不是写给0基础的用户看的（

在阅读前，您至少需要：

+ 有台PC
+ 知道怎么开机
+ 知道怎么用鼠标键盘，知道win键是哪个
+ 知道如何用电脑浏览器下载文件
+ 具有一定的英文基础

## docker一句话部署

> 没有docker的可以根据自己的linux发行版复制然后运行本仓库的安装脚本
>  + [install_docker_debian.sh](install_docker_debian.sh)
>  + [install_docker_centos.sh](install_docker_centos.sh)
> 里面的命令

`docker run -it voidf/irori:v4`

或者如果你嫌国外镜像下载不够快的话：

`docker run -it voidf/irori:v4 --registry-mirror=https://docker.mirrors.ustc.edu.cn`

## 快速部署（精简版）

1. 克隆本仓库
2. 本目录下新建`authdata`,第一行写QQ号，第二行写authKey，第三行写上`[http或https]://[mirai-http-api实例host]:[端口]/`
3. 安装python3，然后`pip3 install -r requirements.txt`
4. 安装java，记得配好环境变量
5. 将[release里的env](http://d0.ananas.chaoxing.com/download/aad7ee20c57d3b402b7f254b4f3373de)文件解压
6. 在解压目录里面`./run.sh`
7. `python3 irori.py`

## 安装使用（啰嗦版）

先装[python](https://www.python.org/downloads/)最好是3.8左右这样的版本,最好是64位，即安装包上写有AMD64字样的exe包

安装时一路往下，记得勾上**加入环境变量**即 **add to PATH** 或者**add to environment variable**什么的，和**pip**。

然后win+R打开cmd或者powershell随你（

用d:,e:这类命令换当前所在的盘，然后一路 `cd 文件夹名` 来达到你想要放压缩包或者将要拷的git仓库的路径（文件夹）里。如果走过了，试试用 `cd ..` 回到上级文件夹。

拷下本仓库，有git最好

`git clone https://github.com/voidf/bot_irori.git`

没有git的话压缩包下载然后解压大概也行？就右上角绿色按钮Clone and download，选择zip下载，然后解压。~~没试过~~

那么我们的cmd也到了这个zip解压的目录

现在先装依赖库

`pip install -r requirements.txt`

解压release里的环境包

双击`run.bat`或者终端敲入`run.sh`就动起来了

然后用你需要当bot的QQ号和密码来登录。

### 配置api

现在来改一下`plugins/MiraiAPIHTTP/setting.yml`

主要改一下你需要的端口`port`和秘钥`authKey` authKey自主选择可能有时候会出锅 那么用它默认的也可以 （稳定性第一 安全性其次~~其实不暴露到外网基本上没必要设置~~

然后现在来告诉irori怎么认证：

在本项目下建一个文件，叫`authdata`,没有后缀，如果win下建不了请打开cmd切到这个目录然后输入

`echo 1 > authdata`

用记事本打开这个文件，（如果没有更好的编辑器的话）在文件第一行写你bot的QQ号，第二行写前面说到的authKey，第三行写上`http://localhost:`+你的port 之后要加上很重要的斜杠/

然后回到本项目目录

`python irori.py`

然后把bot所在qq和你自己拉一个群或者私聊你的bot

输入#h查看帮助

魔改随意，虽然我主要是自己用

~~不会吧不会吧，不会真的有除了我以外的人用这么难用的bot吧~~

## 进阶：cfg.json配置模板

```python
{
    "banGroup": {
        "114514":["#CF"]
    }, # 不允许114514群用#CF命令
    "allowGroup": {
        "1919810": ["#CF","#AT"]
    }, # 仅允许1919810群用#CF，#AT两个命令
    "botList": [
        1926,
        817
    ], # 每个群内忽略QQ号为1926和817的两个群员的发言
    "onlineMsg": {
        "998244353": ["雷真殿に迷惑をかけているのではあるまいな？","ありませんか？"]
    }, # 向群998244353从后面的列表中抽一个字符串发送登录提醒
    "proxy": {
        "http": "socks5://11.4.51.4:810",
        "https": "socks5://11.4.51.4:810"
    }, # 设置代理（目前只有#看看病 用到
    "masters": [233, 666], # 设置系统级命令的管理员（player号
    "enables": [0], # 默认使能状态，0为默认处理任何对象的消息，否则只处理提供的player号
    "appid": "2020123456789", # 设置百度翻译的appid
    "secretKey": "ajusdhgiudhfgiohsdkil", # 百度翻译的密钥
    "echoMsg": false, # 是否打印收到的消息链
    "lengthLim":1919, # 文字转图片的字符串长度阈值
    "AVGHost": "http://127.0.0.1:1919", # AVG主机地址（没有或不需要可留空
    "OJHost": "http://127.0.0.1:14569" # OJ主机地址（没有或不需要可留空
}
```

可以从仓库给定的`cfg.json.template`直接修改，将后缀`.template`和文件里的所有井号注释删去，改为自己合适的设置然后保存即可。

## 系统命令手册

sudo 系列命令只有在消息的发送来源包括在masters内的时候会执行。

| 命令 | 描述 |
| ------ | ----- |
| sudo su | 进入su模式，每条消息都会先判断是否命中系统调用命令 |
| sudo exit | 退出su模式 |
| sudo pull | 从git仓库拉取代码，但新的代码只在reload后生效 |
| sudo reload | 热重载代码，但irori.py, GLOBAL.py, Sniffer.py, Routiner.py这些不会被重载 |
| sudo exec | 执行一条python语句 |
| sudo eval | 执行一条python语句，并返回结果（由于不支持赋值等无返回值操作，故提供exec） |
| sudo pexc | 如果运行时出现异常，则在QQ消息中返回这个异常 |
| sudo cexc | 禁用QQ消息中返回异常 |
| sudo run | 在宿主机上运行一条命令 |
| sudo terminal | 在宿主机上打开一个交互终端 |
| sudo instances | 展示目前在线的所有irori实例 |
| sudo use | `use *` 代表所有实例都会响应消息, `use <uuid>` 可设置仅指定uuid的实例会响应 |


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
