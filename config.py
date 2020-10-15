import platform
import pexpect
import pexpect.popen_spawn



account = input("QQ号？ >>>")
password= input("密码？ >>>")


mirai_console = pexpect.spawn('/env/run.sh')

mirai_console.sendline(f'login {account} {password}')

with open('authdata','w') as f:
    f.write(f"{account}\n1145141919810\nhttp://127.0.0.1:28080/")

with open('irori.py','r') as f: exec(f.read())