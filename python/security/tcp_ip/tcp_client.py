# -*- coding:utf-8 -*-
# tcp_client

import socket

target_url='192.0.0.0'
target_port=9999

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#socket.AF_INETでip4を使うことを指定。socket.SOCK_STREAMでTCPを使うことを指定。

s.connect((target_url,target_port))
#コネクションを確立する。

s.send(b'Hello Server!!!\n')

response = s.recv(4096)
print (str(response))