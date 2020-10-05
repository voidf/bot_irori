# bot-irori 

~~单文件的基于mirai-http-api的bot实例脚本（丑得一逼的排版~~

虽然不再是单文件了但码得还是很乱

mirai项目有时候会出锅 稳定性一般 出问题了重搞亿次就可以了（

## ~~没用的~~features

+ 兼容kuriyama和graia（逃
+ 热重载 `sudo reload`
+ 拉库 `sudo pull`，强制拉库`sudo pull -f`
+ 多实例管理 `sudo use <uuid>`、`sudo instances`
+ QQ群开shell（危
+ QQ群用eval和exec（危
+ 长文字可以渲染为图片发送

## 有那么点点用的功能

+ [x] ddl事件安排及提醒
+ [x] LaTeX公式渲染（其实是爬虫
+ [x] CodeForces、AtCoder、牛客的比赛提醒推送
+ [x] 谷歌翻译，百度翻译（fufu提供的爬虫
+ [x] 答案之书（不知道为什么群友总能玩出新花样

完整功能请部署后使用#h查看

## 前置知识

本篇README不是写给0基础的用户看的（

在阅读前，您至少需要：

+ 有台PC
+ 知道怎么开机
+ 知道怎么用鼠标键盘，知道win键是哪个
+ 知道如何用电脑浏览器下载文件
+ 具有一定的英文基础

## 使用

先装[python](https://www.python.org/downloads/)最好是3.7左右这样的版本,最好是64位，即安装包上写有AMD64字样的exe包

安装时一路往下，记得勾上**加入环境变量**即 **add to PATH** 或者**add to environment variable**什么的，和**pip**。

然后win+R打开cmd或者powershell随你（

用d:,e:这类命令换当前所在的盘，然后一路 `cd 文件夹名` 来达到你想要放压缩包或者将要拷的git仓库的路径（文件夹）里。如果走过了，试试用 `cd ..` 回到上级文件夹。

拷下本仓库，有git最好

`git clone https://github.com/voidf/bot_irori.git`

没有git的话压缩包下载然后解压大概也行？就右上角绿色按钮Clone and download，选择zip下载，然后解压。~~没试过~~

那么我们的cmd也到了这个zip解压的目录

现在先装依赖库

`pip install -r requirements.txt`

**注意kuriyama和graia其实可以只装一个，irori可以只用两者其一，但毕竟用新不用旧，还是下graia罢**

快速配置环境的话可以直接捣鼓一下release里的东西

env本质上是一个[zipx](http://www.bandisoft.com/)压缩包，密码是和*虵*有关，%~~加急~~

解压以后就是整个我自己用的环境了

双击`run.bat`或者终端敲入`run.sh`就动起来了，现在可以直接跳[配置api](https://github.com/voidf/bot_irori#配置api)

~~当然如果你想跟着下面也行~~

接下来有两种方法 如果你想快速上手推荐第一种 如果你想体验像我一样搞几个小时也零成果的~~快感~~ 那么请选第二种

（1）首先去搞[一键包](https://github.com/LXY1226/MiraiOK) 我记得一键包好像是给装Java运行环境的 也可能记错了 如果没有的话 方法二里有装Java的方法 搞完之后 请退出甚至卸载一切杀毒软件（哭 因为~~傻~~杀毒软件会误删你的exe 好的现在你有exe了 你去找一个文件夹把它放进去 然后双击 噼里啪啦出来了一堆 你只需要看最后一行 让你输入qq号 密码 照做就可以 之后你去plugins文件夹下看一下是否有APIHTTP 如果没有 下面有链接 自寻一下 下载下来放进去 然后重启mirai 看到生成一个文件夹 里面有setting.yml 那么就成功了

（2）装java运行环境[Oracle jdk](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html)或者[AdoptOpenJDK](https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.7%2B10.2/OpenJDK11U-jdk_x64_windows_hotspot_11.0.7_10.msi)勾上**JAVA_HOME**（记得配置环境变量**Add to PATH**，不然就得去安装目录像`D:\java\bin\java.exe -jar mirai-console-wrapper-0.2.0-all.jar`这样才能用（

然后去找[mirai-console-wrapper](https://github.com/mamoe/mirai-console-wrapper)

然后在mirai-console-wrapper的jar文件同目录新建或者你运行一次它得到一个plugins这样的目录。

在plugins文件夹里面放[mirai-api-http](https://github.com/mamoe/mirai-api-http/releases)

现在运行mirai-console-wrapper:

`java -jar mirai-console-wrapper-0.2.0-all.jar`

然后会提示要选哪个版本~~反正我只有Pure能用~~，选择自己需要的打上去敲回车就好。

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

大概就能用了（如果炸了试试重启`mirai-console-wrapper-0.2.0-all.jar`,记得千万别关掉这个cmd窗口（

然后把bot所在qq和你自己拉一个群

输入#h查看帮助

魔改随意，虽然我主要是自己用

## 进阶：cfg.json配置模板

```
{
    "banGroup": {
        "114514":["#CF"]
    }, # 不允许114514群用#CF命令
    "allowGroup": {
        "1919810": ["#CF","#AT"]
    }, # 仅允许1919810群用#CF，#AT两个命令
    "Onaji_botList": [
        1926,
        817
    ], # 每个群内忽略QQ号为1926和817的两个群员的发言
    "onlineMsg": [
        [998244353, "雷真殿に迷惑をかけているのではあるまいな？"]
    ], # 向群998244353发送登录提醒“雷真殿に迷惑をかけているのではあるまいな？”
    "proxy": {
        "http": "socks5://11.4.51.4:810",
        "https": "socks5://11.4.51.4:810"
    }, # 设置代理（目前只有#看看病 用到
    "masters": [233, 666], # 设置系统级命令的管理员（player号
    "appid": "2020123456789", # 设置百度翻译的appid
    "secretKey": "ajusdhgiudhfgiohsdkil", # 百度翻译的密钥
    "lengthLim":1919 # 文字转图片的字符串长度阈值
}
```

## 参与开发

参见[DEV.md](DEV.md)

## 老版本kuriyama(0.2.3)留下来的坑

> py安装目录/dist-packages/mirai/event/message/components.py
> 129行和229行
> 
> `- return f"{{{self.imageId.upper()}}}.jpg"`
> 
> `+ return self.imageId.upper()`

> py安装目录/dist-packages/mirai/event/enums.py
> 12行后
> 
> `+ BotLeaveEventActive = "BotLeaveEventActive"`
> 
> `+ BotLeaveEventKick = "BotLeaveEventKick"`

## TODOs:

+ 小坑

+ [ ] 实现生命棋
+ [ ] 实现Fygon计算复杂度
+ [ ] 求二次剩余
+ [ ] 选课

+ 大坑
  
+ [ ] 完善暂时闭源的AVG然后一起开源
+ [ ] ai棋牌
+ [ ] TRPG
+ [ ] irori-OpenJudge

## 引用项目:

[Kumbong/quine_mccluskey](https://github.com/Kumbong/quine_mccluskey)

[be5invis/Sarasa-Gothic](https://github.com/be5invis/Sarasa-Gothic)

## irori的好朋友

[ssttkkl/PixivBot](https://github.com/ssttkkl/PixivBot)

[KutouAkira/bot_fufu](https://github.com/KutouAkira/bot_fufu)

# 你群沙雕日常

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

**欢迎投稿（**