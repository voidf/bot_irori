from graia.application.message.elements.internal import Plain

async def 复读(*attrs, kwargs={}):
    """这是一个复读命令
用法：
    #复读 [某些消息]"""
    return [Plain(' '.join(attrs))]

复读.SHORTS = ['#rep']