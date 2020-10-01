# 写在前面

irori的代码风格**非常扭曲**，如果你不喜欢看长长长长的函数定义和大dict的话请善用折叠和查找功能

比如vscode在每个函数左边有个小箭头

# 基本原理

程序的入口是[irori.py](irori.py),每次的消息会走进那里的监听器。

对于每条消息，她会将其以空格隔开，查找[Callable.py](Callable.py)里面有没有对应的命令，如果有则调用然后退出，没有则下放到查找有没有满足条件的sniffer。

`Callable.py`是热重载的核心，每次收到热重载命令会重载这个文件。所以如果是修改`irori.py`这个入口的话没法热重载，只能自己停止重新运行。

`Callable.py`本质上只是把各个大类的各种函数装进functionMap里，以及函数说明和简写，为它们加上热重载

多提一下，[GLOBAL.py](GLOBAL.py)也不支持热重载。

我的项目包含9个命令大类，可以用#h查看

以及辅助用的`GLOBAL.py`(装全局变量)和[Utils.py](Utils.py)(装一些静态函数)

# 从复读开始

我们随便打开一个类，比如[Generator.py](Generator.py),往里面众多函数下面加一个：

```python
def 复读(*attrs,**kwargs):return [Plain(' '.join(attrs))]
```

然后在底下的`GeneratorMap`里面加入我们希望触发这个函数的命令：

```python
'#repeat':复读
```

这样就建立好了`#repeat`这个消息和函数`复读`之间的联系。

重启`irori.py`,然后向你的bot发送`#repeat 2333`,不出意外的话bot会复读`233`。

> 最好在`GeneratorDescript`下加入`'#repeat'`键值，写上你这个函数的帮助文档，一来可以支持#h查询，二来避免不必要的异常发生

> `GeneratorShort`里装的是函数的简写调用，如果欲有多个命令指向这个函数的话可以通过这个添加

## *attrs

如果你没用过星号表达式，那你应该先百度一下（

这里的`*attrs`装的是命令参数，irori会将每条消息按空格拆开，如下图所示：

![mhtjtmslm](Assets/mhtslm.png)

各个参数会依次塞入`*attrs`,它是一个不定长的tuple,请灵活运用。

## **kwargs

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

这个请直接在`irori.py`的`@irori.subroutine`下面加

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
