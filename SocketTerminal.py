import socket
import traceback
import json

hostname = 'localhost'


with open('cfg.json', 'r',encoding='utf-8') as f:
    jj = json.load(f)
    sport = jj['socket_port']
    del jj

with socket.create_connection((hostname, sport)) as sock:
    # data = sock.recv(1<<16)
    sock.send(b'terminal')

    while 1:
        cmd = input("terminal@irori:/#")
        sock.send(cmd.encode('utf-8'))
        data = sock.recv(1<<16)
        if sock._closed:
            break
        print(data)
    
    # print(data)
    # data = sock.recv(1<<16)
    # print(data)
    # data = sock.recv(1<<16)
    # sock.
    # print(data)

    # with context.wrap_socket(sock, server_hostname=hostname) as ssock:
    #     print(ssock.version())