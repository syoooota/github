# coding:utf-8 
#tcp_server

import socket, threading

bind_ip = '192.0.0.0'
bind_port = 9999


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print( '[*]Listening on %s:%d' % (bind_ip,bind_port))

def handle_client(client_sock):
    request=client_sock.recv(1049)
    ##bufsize=1024

    print('Recived:'+str(request))

    client_sock.send(b'Hello!!\n')

    client_sock.close()

while True:
    client,addr = server.accept()
    #bind済みのソケットから、新たなソケットと接続先のアドレスを返す。
    
    print ('[*] Accepted connectoin from: %s:%d' % (addr[0],addr[1]))

    client_handler = threading.Thread(target=handle_client,args=(client,))
    # threadingを使って、スレッドを生成する。マルチコアに対応させたい場合は,multiprocessingを使えば良い。
    # targetは呼び出す関数(オブジェクト)を指定し、argsはその引数を指定している。
    
    client_handler.start()
    # 処理を開始する。

