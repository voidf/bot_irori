import os
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
from celery import Celery


app = Celery(
    'test3_celery', 
    # broker='pyamqp://guest@localhost//', 
    # backend="mongodb://127.0.0.1:27017/irori_taskqueue",

)
app.config_from_object('celeryconfig')

from basicutils.socketutils import *
from loguru import logger
import traceback

@app.task
def task(s: str):
    """热更新测试通过"""
    ent = CoreEntity.handle_json(s)
    res = sub_task(ent)
    logger.critical(res)
    ent.chain = res
    return ent.json()

@app.task
def pull():
    cmdres = os.popen('git pull').read()
    return cmdres

def sub_task(task: CoreEntity) -> MessageChain:
    import os
    import importlib
    import inspect
    import re
    try:
        app_dir = 'basicutils/applications/'
        app_doc = {}
        app_fun = {}
        tot_funcs = {}
        tot_alias = {}
        # @logger.catch
        def printHelp(chain: MessageChain, meta: dict = {}):
            """不传参打印命令表，传参则解释命令"""
            kwargs = meta
            cop = chain.onlyplain()
            attrs = cop.split(' ')
            logger.warning(attrs)
            show_limit = int(kwargs.get('-showlim', 20))
            l = []
            img = []
            ext = []
            if not attrs or not cop:
                l.append('已导入的模块：')
                for k, v in app_doc.items():
                    l.append(f'''\t{k} {v}''')
                l.append('''输入#h <模块名> 以查询模块下命令
        使用#h <命令名> 可以查询详细用法
        使用#h search <关键字> 可以按照关键字查找相关命令
        尖括号表示参数必要，方括号表示参数可选，实际使用中不必一定需要
        使用#h #abb可以查询缩写表

        通用选项：
            --fi --force-image 强制把文本消息转换成图片发送
            --paste 强制把文本消息粘贴至ubuntu pastebin
            --tts 【试验阶段】强制把消息转换成语音发送
            --voice 【试验阶段】如果命令支持的话，发送语音消息''')
            else:
                if attrs[0] in tot_alias:
                    attrs = [tot_alias[attrs[0]],*attrs[1:]]
                if attrs[0] in tot_funcs:
                    l.append(tot_funcs[attrs[0]].__doc__)
                elif attrs[0] == '#abb':
                    l.append(f'可用缩写表:{tot_alias}')
                # elif attrs[0] in ('all', 'old'):
                #     l.append('可用命令表：')
                #     for k in tot_funcs:
                #         l.append('\t'+k)
                #     l.append('使用#h 命令名（带井号）可以查询详细用法')
                #     l.append('使用#h #abb可以查询缩写表')
                #     l.append('注命令后需打空格，之后的参数如存在空格即以空格分开多个参数，如#qr 1 1 4 5 1 4')
                #     img.append(generateImageFromFile('Assets/muzukashi.png'))
                elif attrs[0] in app_fun:
                    l.append(f'分类：{attrs[0]}')
                    for k, v in app_fun[attrs[0]].items():
                        print(f'descLen = {len(v.__doc__.strip()[:show_limit])}')
                        l.append(f'''\t{k}\t{v.__doc__.strip()[:show_limit]
                        if len(v.__doc__.strip()[:show_limit])<=show_limit
                        else v.__doc__.strip()[:show_limit]+'...'}\n''' )
                elif attrs[0] == "search" and len(attrs) > 1:
                    key = attrs[1]
                    for k, v in tot_funcs.items():
                        if re.search(key, k, re.S) or re.search(key, v.__doc__, re.S):
                            l.append(f'''\t{k}\t{v.__doc__.strip()}\n''' )
                    if not l:
                        l = ["没有结果喵"]
                else:
                    l.append('【错误】参数不合法\n')
                    ext = printHelp(MessageChain.get_empty())
                
            return [Plain('\n'.join(l))] + img + ext

        for applications in os.listdir(app_dir):
            logger.debug(f'importing ... {applications}')
            pkgname = os.path.splitext(applications)[0]
            if os.path.isdir(app_dir + applications):
                continue
            # if pkgname == '__pycache__': continue
            module = importlib.import_module(app_dir.replace('/', '.')+pkgname)
            importlib.reload(module)
            names = module.__dict__.get("__all__", [x for x in module.__dict__ if x[:1] != '_'])
            globals().update({k: getattr(module, k) for k in names})

            funcs = {}
            alias = {}
            helps = {}

            for n, f in inspect.getmembers(module): # 判断这是个可以加进QQ消息调用表的函数
                if not inspect.isbuiltin(f):
                    try:
                        argsinfo = inspect.getfullargspec(f)
                    except TypeError:
                        # logger.debug(f'\t ignoring {n}')
                        continue
                    if argsinfo.args == ['chain', 'meta']:
                        logger.info(f'\t imported {n}')
                        header, f.__doc__ = f.__doc__.split('\n', 1)
                        fname, *ato = header.split(' ', 1)
                        # print(ato)
                        ato = ato[0] if ato else ''
                        try:
                            L, R = ato.index('['), ato.rindex(']')
                            # funcs.update({fname: f})

                            for ss in ato[L+1:R].split(','):
                                ss = ss.strip()
                                if not ss: continue
                                if ss not in alias and ss not in funcs:
                                    alias.update({ss: fname})
                        except ValueError:
                            fname = n
                        funcs.update({fname: f})
                        helps[fname] = f.__doc__
                        print(funcs)
                    # else:
                        # logger.debug(f'\t ignoring {n}')
            app_fun[pkgname] = funcs
            app_doc[pkgname] = module.__doc__
            tot_funcs.update(funcs)
            tot_alias.update(alias)

        tot_funcs['#h'] = printHelp

        logger.debug(tot_funcs)
        logger.debug(tot_alias)

        logger.debug(task)

        cmd = task.chain.pop_first_cmd()
        cmd = tot_alias.get(cmd, cmd)

        logger.debug(f'command: {cmd}')
        if cmd in tot_funcs:
            try:
                reply = tot_funcs[cmd](task.chain, task.meta)
            except:
                reply = MessageChain.auto_make(traceback.format_exc())
            if not reply:
                return MessageChain.get_empty()
            if not isinstance(reply, MessageChain):
                reply = MessageChain.auto_make(reply)
            # elif isinstance(reply, Plain):
            #     reply = MessageChain(__root__=[reply])
            # elif isinstance(reply, list):
            #     reply = MessageChain.auto_make
            # else:
                # reply = MessageChain(__root__=[str(reply)])
            return reply
        return MessageChain.get_empty()
    except:
        logger.error(traceback.format_exc())
        return MessageChain.auto_make(traceback.format_exc())