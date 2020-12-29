from graia.application.message.elements.internal import Plain

async def 复读(*attrs, kwargs={}):
    return [Plain(' '.join(attrs))]