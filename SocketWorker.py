import socket

import argparse

hostname = 'localhost'

with open('cfg.json', 'r',encoding='utf-8') as f:
    jj = json.load(f)
    sport = jj['socket_port']
    del jj

import traceback
from multiprocessing.dummy import Pool as Pool2
def task_monitor(func, *args, **kwargs):
    tle = kwargs.get('tle', None)
    p = Pool2(1)
    res = p.apply_async(func, args=args)
    pid = kwargs['pid']
    # print(kwargs)
    try:
        out = res.get(tle)
        # kwargs['worker'].release()

        tmpd = kwargs['pcb'][pid]
        tmpd['status'] = 'done'
        kwargs['pcb'].update({pid:tmpd})
        # kwargs['pcb'][pid].update(status='done')
        # print(kwargs)
        print(pid, '执行完毕, 结果：', out)
        return out
    except:
        traceback.print_exc()
        # kwargs['worker'].release()

        tmpd = kwargs['pcb'][pid]
        tmpd['status'] = 'timeout'
        kwargs['pcb'].update({pid:tmpd})
        print(pid, '执行超时')

with socket.create_connection((hostname, sport)) as sock:
    # data = sock.recv(1<<16)
    sock.send(b'worker')
    data = sock.recv(1<<16)
    # print(data)
    # data = sock.recv(1<<16)
    # print(data)
    # data = sock.recv(1<<16)
    # sock.
    # print(data)

    # with context.wrap_socket(sock, server_hostname=hostname) as ssock:
    #     print(ssock.version())

# <?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID="107" templateID="1" action="viewReceiptMessage" brief="[回执消息]" m_resid="UUAq5xccO44DIuoF23YLkxMk04EBBbGxESP6o45SqHb2KiUOmUpPUHoBkBSUwKcL" m_fileName="6862690782327914927" sourceMsgId="0" url="" flag="3" adverSign="0" multiMsgFlag="0"><item layout="29" advertiser_id="0" aid="0"><type>1</type></item><source name="" icon="" action="" appid="-1" /></msg>
# <?xml version='1.0' encoding='UTF-8' standalone='yes' ?><msg serviceID=\"2\" templateID=\"1\" action=\"web\" brief=\"[分享] China-P\" sourceMsgId=\"0\" url=\"https://y.qq.com/n/yqq/song/00222Pi34ZJlkr.html\" flag=\"0\" adverSign=\"0\" multiMsgFlag=\"0\"><item layout=\"2\"><audio cover=\"http://y.gtimg.cn/music/photo_new/T002R300x300M000004Kr0bo3ayyfH_1.jpg?max_age=2592000\" src=\"http://122.226.161.16/amobile.music.tc.qq.com/M80000222Pi34ZJlkr.mp3?guid=1712873&amp;vkey=2B4EDCF49FFE21F599CAB423322B3EC49D119B9C8F770F1AE2E76F05BB8B0890F5D287930E2FBC6856D9124DDCBB4F7DC2CCC761AE3D196A&amp;uin=1899&amp;fromtag=66\" /><title>China-P</title><summary>徐梦圆</summary></item><source name=\"QQ音乐\" icon=\"https://i.gtimg.cn/open/app_icon/01/07/98/56/1101079856_100_m.png?date=20200503\" url=\"http://web.p.qq.com/qqmpmobile/aio/app.html?id=1101079856\" action=\"app\" a_actionData=\"com.tencent.qqmusic\" i_actionData=\"tencent1101079856://\" appid=\"1101079856\" /></msg>

# <?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
# <msg serviceID=\"2\" templateID=\"1\" action=\"web\" brief=\"[分享] China-P\" sourceMsgId=\"0\" 
# url=\"https://y.qq.com/n/yqq/song/00222Pi34ZJlkr.html\" flag=\"0\" adverSign=\"0\" multiMsgFlag=\"0\"><item layout=\"2\">
# <audio cover=\"http://y.gtimg.cn/music/photo_new/T002R300x300M000004Kr0bo3ayyfH_1.jpg?max_age=2592000\" src=\"http://122.226.161.16/amobile.music.tc.qq.com/M80000222Pi34ZJlkr.mp3?guid=1712873&amp;vkey=2B4EDCF49FFE21F599CAB423322B3EC49D119B9C8F770F1AE2E76F05BB8B0890F5D287930E2FBC6856D9124DDCBB4F7DC2CCC761AE3D196A&amp;uin=1899&amp;fromtag=66\" /><title>China-P</title><summary>徐梦圆</summary></item><source name=\"QQ音乐\" icon=\"https://i.gtimg.cn/open/app_icon/01/07/98/56/1101079856_100_m.png?date=20200503\" url=\"http://web.p.qq.com/qqmpmobile/aio/app.html?id=1101079856\" action=\"app\" a_actionData=\"com.tencent.qqmusic\" i_actionData=\"tencent1101079856://\" appid=\"1101079856\" />
# </msg>

