import platform
import pexpect
import pexpect.popen_spawn
import os


account = input("QQ号？ >>>")
password= input("密码？ >>>")


desc = """
成功进入shell
手动配置教程：
    1. 进入/env/
        > 如果你没用过linux的话，用"cd /env"(不带引号)来进入这个目录
    2. 根据需要调节/env/plugins/MiraiAPIHTTP/setting.yml
        > 如果你没用过linux的话，用"nano /env/plugins/MiraiAPIHTTP/setting.yml"(不带引号)然后通过方向键和键盘编辑这个文本
    3. 主要调节port的值，确保你填的端口没被占用，authKey如果你真的改了这个向导很可能会用不了
    4. 调好后保存文件退出
        > 如果你没用过nano的话，CTRL+s保存文件，然后CTRL+x退出
    5. 后台运行"/env/run.sh"
        > 如果你不会用后台，"screen -R mirai"，然后"/env/run.sh"，然后CTRL+a然后敲一下d
    6. 输入exit退回向导，或者如果你愿意的话可以进入/irori折腾（
"""

cmd = ''

authkey = '1145141919810'
os.chdir('/env')
mirai_console = pexpect.spawn('bash /env/run.sh')

mirai_console.sendline(f'login {account} {password}')

try:
    while cmd not in ('DONE','BASH'):
        try:
            mirai_console.sendline(cmd)
            while True:
                mirai_console.expect('\r\n',timeout = 3)
                print(mirai_console.before.decode('utf-8'))
        except:
            cmd = input('上面是mirai_console的输出，\n如果你觉得已经没问题的话请输入"DONE"来启动irori，\n或者输入"BASH"来开启一个shell进行手动配置。除了"BASH"和"DONE"之外的所有输入会被转发至mirai终端>>>')
    if cmd == 'BASH':
        print(desc)
        os.system('bash')
        t = input('您刚才有修改authKey吗？如果有请现在输入新的authKey，否则留空>>>')
        if t: authkey = t
except KeyboardInterrupt:
    print('irori启动...')

os.chdir('/irori')
with open('authdata','w') as f:
    f.write(f"{account}\n{authkey}\nhttp://127.0.0.1:28080/")

with open('irori.py','r') as f: exec(f.read())