# coding:utf-8

import threading, paramiko, sys, socket, os

host_key=paramiko.RSAKey(filename="test_rsa.key")

class Server (paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()
    def check_channel_request(self, kind, chanid):
        if kind == b'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_passward(self, username, password):
        print(username)
        if(username == b'justin') and (password == b'lovesthepyhon'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print("[+] Listening for connection ...")
    client, addr = sock.accept()
except Exception as e:
    print("[-] Listen failed: " + str(e))
    sys.exit(1)
print("[+] Got a connection!")

try:
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(host_key)
    server = Server()
    try:
        bhSession.start_server(server=server)
    except paramiko.SSHException as x:
        print("[-] SSH negotiation failed.")
    chan = bhSession.accept(20)
    print("[+] Authenticated!")
    print(chan.recv(1024).decode('shift_jis'))
    pr
    chan.send(b'Welcome to bh_ssh')
    
    while True:
        try:
            command = input("Enter command: ").strip('\n')
            if command != b'exit':
                chan.send(command)
                print(chan.recv(1024).decode('shift_jis') + '\n')
            else:
                chan.send(b'exit')
                print('exiting')
                bhSession.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            bhSession.close()
except Exception as e:
    print("[-] Caught exeception: " + str(e))
    try:
        bhSession.close()
    except:
        pass
    sys.exit(1)
    

        