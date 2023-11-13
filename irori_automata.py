import re
import os
import sys
import aiohttp
import asyncio
import keyboard
from pywinauto.findwindows import find_elements
from pywinauto import Application
import tkinter as tk
import win32clipboard as wcb
from collections import deque
from dotenv import load_dotenv
import win32con

load_dotenv()

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

w = app.window(title_re="消息管理器")
# w.print_control_identifiers()

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

def click_refresh_btn(w):
    sonlist = [2, 0, 1, 0, 2, 0, 1, 0]
    child = get_child(w, sonlist[0])
    for x in sonlist[1:]:
        child = get_child(child, x)
    child.click_input() # 模拟鼠标点击

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

def fetch_msg(w):
    click_refresh_btn(w)
    li = w.child_window(title="IEMsgView", control_type="List")
    list_items = li.children(control_type="ListItem")
    pending_msg = []
    for p, item in enumerate(list_items):
        content = item.window_text()
        r = pat.match(content)
        if r:
            groups = r.groups()
            sender_qid_found = pat_qid.search(groups[0])
            sender = ''
            if sender_qid_found:
                sender = sender_qid_found.group(1)
            else:
                sender_email_found = pat_email.search(groups[0])
                if sender_email_found:
                    sender = sender_email_found.group(1)

            if not sender:
                print('not found sender id:', p, content)
            else:
                if sender != read_secret("BOT_ID"): # 屏蔽自己
                    if insert_msg(sender + '-' + ':'.join(groups[1:4])):
                        pending_msg.append((sender, groups[4]))
        else:
            print('not found', p, content)
    return pending_msg
        # print(p, item.window_text())

def send_msg(app, t: str = 'test'):
    w = app.window(title_re=read_secret('WINDOW_TITLE'))
    edit_ctrl = w.child_window(title="输入", control_type="Edit")
    edit_ctrl.click_input()
    wcb.OpenClipboard()  # 打开剪贴板
    wcb.EmptyClipboard()  # 清空剪贴板
    wcb.SetClipboardData(win32con.CF_UNICODETEXT, t)  # 设置剪贴板数据
    wcb.CloseClipboard()  # 关闭剪贴板
    # pyperclip.copy(t)
    edit_ctrl.type_keys("^v")
    # edit_ctrl.type_keys(t, with_spaces=True, with_newlines=True)
    w.child_window(title="发送(&S)", control_type="Button").click_input()

async def main():
    login_token = read_secret('LOGIN_TOKEN')
    register_player_id = read_secret('REG_PID')
    fetch_msg(w)
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(read_secret("WS_URL").format(login_token, register_player_id)) as ws:
            async def on_recv_msg(msg):
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        print(f"Received message: {msg.json()}")
                        send_msg(app, msg.data)
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
                    await asyncio.sleep(0.1)
                    pending_msg = fetch_msg(w)
                    for sender, msg in pending_msg:
                        await ws.send_json({
                            'chain':msg,
                            'mid':sender
                        })
            scan_task = asyncio.create_task(loop_scan_msg())
            await on_recv_msg(ws)
            scan_task.cancel()
            exit(1)

if __name__ == "__main__":
    asyncio.run(main())