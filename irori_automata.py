import re
import os
import sys
import datetime
from typing import List, Tuple
import aiohttp
import asyncio
import keyboard
import xml.etree.ElementTree as ET
from pywinauto.findwindows import find_elements
from pywinauto import Application
import tkinter as tk
import win32clipboard as wcb
from collections import deque
from dotenv import load_dotenv
import win32con

from basicutils.network import CoreEntity
from basicutils.chain import MessageChain, Plain, Image

load_dotenv()

QQRichEditFormat = 49769

def read_secret(key: str) -> str:
    v = os.environ[key] = os.environ.get(key) or input(f"Please input {key}:")    
    return v

def draw_rectangle(x, y, width, height):
    width = width - x
    height = height - y
    # 创建 Tkinter 窗口
    root = tk.Tk()
    root.overrideredirect(True)  # 隐藏窗口边框和标题栏
    root.geometry(f"{width}x{height}+{x}+{y}")  # 设置窗口大小和位置

    # 使窗口透明
    root.attributes('-alpha', 0.9)  # 设置透明度

    # 在窗口上绘制矩形
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()
    canvas.create_rectangle(0, 0, width, height, outline='#00FF00', fill='#00FF00')

    # 显示窗口并在一段时间后自动关闭
    root.after(3000, root.destroy)  # 5秒后销毁窗口
    root.mainloop()


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
    return data_map

elements = find_elements(title='QQ', class_name=None)
print(elements)
print('connect to', elements[0].process_id)
app = Application(backend="uia").connect(process=elements[0].process_id)

def get_child(w, idx):
    chl = w.children()
    # print(chl)
    return chl[idx]

def get_sub(w):
    child = get_child(w, 2)
    # print(child, child.automation_id())
    # child_spec = w.child_window(auto_id=child.automation_id(),)
    # child_spec.draw_outline()
    # child_spec.print_control_identifiers()
    child.click_input() # 模拟鼠标点击
    return child

pat = re.compile(r'^(.*?)(\d{1,2}):(\d{1,2}):(\d{1,2})(.*)$', re.M | re.S)
pat_qid = re.compile(r'\((\d{1,10})\)$')
pat_email = re.compile(r'<(\w+@\w+\.\w+)>$')

msg_queue = deque()
msg_set = set()

QUEUE_LIMIT = 100

def insert_msg(msg: str) -> bool:
    if msg in msg_set:
        return False
    msg_set.add(msg)
    msg_queue.append(msg)
    while len(msg_queue) > QUEUE_LIMIT:
        msg_set.remove(msg_queue.popleft())
    return True

def extract_sender_id(sender_str: str):
    sender_qid_found = pat_qid.search(sender_str)
    sender = ''
    if sender_qid_found:
        sender = sender_qid_found.group(1)
    else:
        sender_email_found = pat_email.search(sender_str)
        if sender_email_found:
            sender = sender_email_found.group(1)
    return sender

async def fetch_msg(app):
    w = app.window(title_re=read_secret('WINDOW_TITLE'))
    li = w.child_window(title_re='消息', control_type='List')
    li.click_input()
    await asyncio.sleep(0.3)
    li.click_input()
    await asyncio.sleep(0.3)
    li.type_keys('^a')
    await asyncio.sleep(0.3)
    li.type_keys('^c')
    await asyncio.sleep(0.3)
    data_map = get_clipboard_data()
    pending_msg = []

    for sender, sender_time_str, msgchain in parse_rtf(data_map[QQRichEditFormat].decode('utf-8')):
        sender_id = extract_sender_id(sender)
        if sender_id != read_secret("BOT_ID"): # 屏蔽自己
            if insert_msg(sender_id + '-' + sender_time_str):
                pending_msg.append((sender_id, msgchain))
    return pending_msg


sender_pat = re.compile(r'(.*?) (20\d{2}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})$')

def parse_rtf(data: str) -> List[Tuple[str, str, MessageChain]]:
    print(datetime.datetime.now(), 'bytes:', len(data))
    root = ET.fromstring(data)
    ret = []
    current_sender = None
    current_send_time = None
    buf = []
    for element in root.findall('.//EditElement'):
        element_type = element.get('type')
        if element_type == '0':  # 文本消息
            text = element.text.strip() if element.text else ''
            for line in text.splitlines():
                sender_match = sender_pat.search(line)
                if sender_match:
                    if current_sender and buf:
                        ret.append((current_sender, current_send_time, MessageChain.auto_make(buf)))
                    current_sender, current_send_time = sender_match.groups()
                    buf.clear()
                else:
                    buf.append(Plain(text=line + '\n'))
        elif element_type == '1':  # 图片
            buf.append(Image(path=element.get('filepath')))
    if current_sender and buf:
        ret.append((current_sender, current_send_time, MessageChain.auto_make(buf)))
    return ret

def dump_rtf(msgchain: MessageChain):
    out = []
    for elem in msgchain:
        if isinstance(elem, Plain):
            out.append('<EditElement type="0"><![CDATA[' + elem.text + ']]></EditElement>')
        elif isinstance(elem, Image):
            out.append('<EditElement type="1" imagebiztype="0" textsummary="" filepath="' + elem.path + '" shortcut=""></EditElement>')
    wcb.OpenClipboard()  # 打开剪贴板
    wcb.EmptyClipboard()  # 清空剪贴板
    wcb.SetClipboardData(QQRichEditFormat, '<QQRichEditFormat><Info version="1001"></Info>' + ''.join(out) + '</QQRichEditFormat>')  # 设置剪贴板数据
    wcb.CloseClipboard()  # 关闭剪贴板

def send_msg(app, msgchain: MessageChain):
    w = app.window(title_re=read_secret('WINDOW_TITLE'))
    edit_ctrl = w.child_window(title="输入", control_type="Edit")
    edit_ctrl.click_input()
    dump_rtf(msgchain)
    edit_ctrl.type_keys("^v")
    # edit_ctrl.type_keys(t, with_spaces=True, with_newlines=True)
    w.child_window(title="发送(&S)", control_type="Button").click_input()

async def main():
    login_token = read_secret('LOGIN_TOKEN')
    register_player_id = read_secret('REG_PID')
    await fetch_msg(app)
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(read_secret("WS_URL").format(login_token, register_player_id)) as ws:
            async def on_recv_msg(msg):
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        j = msg.json()
                        print(f"Received message: {j}")
                        msgchain = MessageChain.parse_obj(j['chain'])
                        send_msg(app, msgchain)
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        print('ws closed', msg)
                        break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        print('ws error', msg)
                        break
                    else:
                        print("?", msg.type, msg.data)
            async def loop_scan_msg():
                while 1:
                    await asyncio.sleep(3)
                    pending_msg = await fetch_msg(app)
                    for sender, msg in pending_msg:
                        print(sender, msg)
                        await ws.send_json({
                            'chain':msg,
                            'mid':sender
                        })
            scan_task = asyncio.create_task(loop_scan_msg())
            await on_recv_msg(ws)
            scan_task.cancel()
            exit(1)


# from pathlib import Path
# {"chain":[{"type":"Plain","meta":{"delay":0},"text":"[4, 12, '*']\n(4*12) = 48"}]}
if __name__ == "__main__":
    asyncio.run(main())