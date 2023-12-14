import fastapi
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
import keyboard
import datetime
import time
import win32clipboard as wcb
import win32api

last_access = datetime.datetime.now() - datetime.timedelta(seconds=7200)

app = FastAPI()

class Msg(BaseModel):
    m: str

def get_clipboard_data():
    wcb.OpenClipboard()
    # 枚举剪贴板中的所有格式
    format = 0
    data_map = {}
    while True:
        format = wcb.EnumClipboardFormats(format)
        if not format:
            break
        try:
            data = wcb.GetClipboardData(format)
            data_map[format] = data
        except Exception as e:
            print(f"Error getting data for format {format}: {e}")
    wcb.CloseClipboard()
    print(data_map)
    return data_map

@app.post('/i')
async def _(msg: Msg):
    global last_access
    now = datetime.datetime.now()
    gap = (now - last_access).total_seconds()
    print(gap)
    if gap < 72:
        rep = '等一下捏，72秒能请求一次，还差{}秒'.format(72 - gap)
        print(rep)
        return [rep]
    last_access = now

    inputmsg = msg.m
    print(inputmsg)
    time.sleep(0.5)
    print('start')
    print(wcb.CF_UNICODETEXT)

    wcb.OpenClipboard()  # 打开剪贴板
    wcb.EmptyClipboard()  # 清空剪贴板
    wcb.SetClipboardData(wcb.CF_UNICODETEXT, inputmsg)
    wcb.CloseClipboard()  # 关闭剪贴板

    keyboard.send('shift+esc')
    time.sleep(0.1)
    keyboard.send('ctrl+v')
    time.sleep(0.1)
    keyboard.send('enter')
    time.sleep(12)

    prev = ''
    while 1:
        keyboard.send('ctrl+shift+c')
        time.sleep(0.3)
        curr = get_clipboard_data()[wcb.CF_UNICODETEXT]
        if curr == prev:
            break
        prev = curr
        time.sleep(5)
    return [prev]

if __name__ == "__main__":
    uvicorn.run(app, port=11111) # 7007