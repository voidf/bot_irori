# 写在前面

irori面向过程，代码风格**非常扭曲**，如果你不喜欢看长长长长的函数定义和大dict的话请善用代码折叠和查找功能

比如vscode在每个函数左边有个小箭头


# 项目结构

| 文件 | 存在意义 |
| --- | --- |
| authdata | 指定登录必须的认证信息和mirai-http-api地址 |
| cfg.json | 全局策略设置文件，参见README.md |
| irori.py | 程序的主入口 |
| Fetcher.py | 爬虫函数包 |
| Utils.py | 功能性函数包（待拆分） |
| Callable.py | 热重载的核心，将扫描到的插件导入到命令映射表 |
| Routiner.py | 订阅业务和定时任务的核心 |
| Sniffer.py | 监听器消息处理核心 |
| plugins/ | 插件文件夹 |
| config.py | 仅仅是用于docker快速部署用到的小脚本，与主程序无关 |

# 基本原理

程序的入口是[irori.py](irori.py),每次的消息会走进那里的监听器。

对于每条消息，她会将其以空格隔开，将双减号开头的参数解析并塞入extDict然后查找[Callable.py](Callable.py)里面有没有对应的命令，如果有则调用然后退出，没有则下放到查找有没有满足条件的sniffer。

`Callable.py`是热重载的核心，每次收到热重载命令会重载这个文件。所以其实只有Callable里面涉及到的包会重载，即plugins目录下的所有插件以及Callable本身。

`Callable.py`执行的工作是只是将plugins下所有业务代码载入命令映射表。命令调用的主题在入口irori.py处进行

项目本身包含9个自带插件，可以用#h查看

# 我就是想让她动起来

我们在[plugins/](plugins/)下建一个py文件，比如[myplugin.py](plugins/myplugin.py)然后照着以下这么写

```python
from graia.application.message.elements.internal import Plain

async def 复读(*attrs, kwargs={}):
    return [Plain(' '.join(attrs))]
```

这样你就可以直接使用命令`#复读`来调用`复读`这个函数

重启`irori.py`或者使用`sudo reload`,然后向你的bot发送`#复读 2333`,不出意外的话bot会复读`2333`。

# 我想让别人知道我的命令怎么用

只需要在我们的例子中，为业务函数加上`__doc__`即文档字符串即可。具体操作如下：

```python
from graia.application.message.elements.internal import Plain

async def 复读(*attrs, kwargs={}):
    """这是一个复读命令
用法：
    #复读 [某些消息]"""
    return [Plain(' '.join(attrs))]
```

这样一来使用时就可以通过`#h #复读`来查询到这个命令的帮助了。

# 我同一个函数想使用多个命令来调用

我们可以在函数下方为函数指定属性`SHORTS`，如下：

```python
from graia.application.message.elements.internal import Plain

async def 复读(*attrs, kwargs={}):
    """这是一个复读命令
用法：
    #复读 [某些消息]"""
    return [Plain(' '.join(attrs))]

复读.SHORTS = ['#rep']
```

`SHORTS`属性必须是一个列表，里面提供的所有字符串会被alias到这个函数里。注意这里不能像函数名一样忽略开头的#号，否则如上打成`rep`则消息需以`rep 2333`的形式才能触发上述效果


## *attrs

如果你没用过星号表达式，那你应该先百度一下（

这里的`*attrs`装的是命令参数，irori会将每条消息按空格拆开，如下图所示：

![mhtjtmslm](Assets/mhtslm.png)

各个参数会依次塞入`*attrs`,它是一个不定长的tuple,请灵活运用。

## kwargs

捕获一些额外信息的不定长字典，常用的有：

`player`:发送对象的player号

`mem`:发送对象的QQ，是一个Member对象，可以通过.id拿到qq号

`gp`:只在群组消息会有，消息来源群的群对象(Group)，可以通过.id拿到群号

`pic`:消息中包含的第一张图片的url

还有各种带`-`号的可选参数，参见[可选参数](可选参数)

## 关于player号

player号事irori中根据群或者好友来源qq号生成的一种统一号。用于消息分发等地方。算法事好友消息即好友的qq号，群组消息则事群组qq号加上1<<39

如果有获取player号的需求，直接调用Utils下的getPlayer方法，将**kwargs直接扔进去即可

如：

```python
player = getPlayer(**kwargs)
```

## 可选参数

在消息的预处理中，每段以`-`或者`--`开头的参数不会被扔进`*attrs`里。它们会被装进**kwargs里以键值对的形式传递。参见以下几个例子：

```
#线代 mul 1,1,4;5,1,4;1,9,1 2,2,3;4,4,5;3,3,1 --force-image
```

此时`*attrs`里装的是
```python
("mul","1,1,4;5,1,4;1,9,1","2,2,3;4,4,5;3,3,1")
```

`**kwargs`里装有
```python
{"-force-image":""}
```

```
#线代 mul 1,1,4;5,1,4;1,9,1 --force-image -theme=114 2,2,3;4,4,5;3,3,1
```

此时`*attrs`里装的是
```python
("mul","1,1,4;5,1,4;1,9,1","2,2,3;4,4,5;3,3,1")
```

`**kwargs`里装有
```python
{"-force-image":"","-theme":"114"}
```

请灵活使用这种参数

## 登录任务

这个请直接在`irori.py`的`hajime`函数下面加

# Utils相关

## 异步消息分发

可以使用Utils下的msgDistributer异步方法

它接受不定长键值型传参

下面给出了几个例子：

```python
asyncio.ensure_future(msgDistributer(msg="文字",typ="P",player=114514))
```

向player号为114514的老铁发送`文字`这么个文本消息

```python
asyncio.ensure_future(msgDistributer(msg="kuaikule",typ="E",player=114514))
```

![kuaikule](Assets/kuaikule.png)

```python
asyncio.ensure_future(msgDistributer(msg="https://i.pximg.net/img-original/img/2020/09/27/19/46/09/84651430_p0.jpg",typ="I",player=114514))
```

发![夸的新衣服](https://i.pximg.net/img-original/img/2020/09/27/19/46/09/84651430_p0.jpg)这么一张图（挺灵车的功能

```python
asyncio.ensure_future(msgDistributer(msg="<base64编码的图片>",typ="I",player=114514))
```

以base64编码形式发送图片

```python
asyncio.ensure_future(msgDistributer(msg="/home/irori/wakaru.png",typ="I",player=114514))
```

以本地文件目录的形式发送图片

## 文件操作

因为v3的限制，Image大概只能本地文件发送，可以使用Utils下的randstr生成临时文件名，参数为随机字符串长度，然后将文件名扔入rmTmpFile异步方法让这个临时文件在一段时间后删除

例：

```python
fn = 'tmp' + randstr(8)
with open(fn,'w') as f:
    f.write("something\n")
asyncio.ensure_future(rmTmpFile(fn))
return Image.fromFileSystem(fn)
```

## 使用sniffer

sniffer是检测消息是否存在触发的关键词来决定对应函数要不要被调用的一种机制，过多的sniffer会降低程序处理速度，因为对于每条消息都要O(n)检索

新建一个sniffer，可以使用Utils下的overwriteSniffer方法，用例：

```python
overwriteSniffer(114514,'#repeat','.*','复读：')
```

解释一下：

+ 第一个参数是player，即需要添加sniffer的player号，是int

+ 第二个参数是满足条件后调用的命令

+ 第三个参数是一个正则串，如果发送的消息能被这个正则串匹配，则会触发这个方法

+ 之后的参数是不定长参数，他们会添加于命令之后，然后再将源消息当做参数加入

比如假设你执行了上面的一句

然后你向irori发送`LALALA 233`这么一条文本消息，由于`.*`被匹配成功，bot处理的时候会视为这么一条消息：

```
#repeat 复读： LALALA 233
```

如果要为一条sniffer添加一个监听关键词，可以使用Utils下的appendSniffer方法。与overwriteSniffer接受参数唯一的不同就是它没有最后那个不定长参数

```python
appendSniffer(114514,'#repeat','\?')
```

删掉对某个事件的所有sniffer可以使用Utils下的removeSniffer方法。

```python
removeSniffer(114514,'#repeat')
```

## 使用超星网盘

有些时候做出来的文件不太方便传出去（还没搞出群文件或者私聊文件的接口）那么我们可以把文件传到超星网盘供用户下载。

使用Utils下的uploadToChaoXing方法，传入文件的本地路径，返回的是文件的超链接

但注意超星网盘单个文件不能超过200M

# 设置运行版本

可以在GLOBAL文件中设置irori使用的python-mirai环境，默认是4（即graia

可以调成3来在kuriyama下继续运行irori

# 发送图片

为了v3和v4的兼容，最好走Utils下的generateImageFromFile方法

当然如果你自己特别想用v4特性我也不拦你就是了（

# 全局变量

由于到处都有import GLOBAL，所以尽管把需要的东西往GLOBAL里放

# 对接AVG

这是一个大坑，我们的其实还不太成型，这里先不讨论。

配置AVG需要在本目录下新建一个`hakushinAVG.txt`

然后写上AVG的接口地址，然后换行写上端口

比如我是这么写的：

```
127.0.0.1
1919
```

这部分因为耦合度太高之后要大力重构

# 创建你自己的新命令大类

建议从已有的类中拷过去改，只需要把文件名改一下，底下的三个dict改一下名，然后去Callable.py里面加一下关联，你就可以用你自己的大类玩了
