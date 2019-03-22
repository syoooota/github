# coding:utf-8

import os, socket,struct
from ctypes import *
import threading, time
from netaddr import IPNetwork, IPAddress

host = "192.0.0.0"
subnet = "192.0.0.0/24"

magic_message = "PYTHONRULES!"

def udp_sender(subnet, magic_message):
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    for i in IPNetwork(sender):
        try:
            sender.sendto(magic_message, ("%s" % ip,65212))
        except:
            pass


class IP(Structure):
    _fields_ = [
             ("ihl",          c_uint8, 4),
             ("version",      c_uint8, 4),
             ("tos",          c_uint8),
             ("len",          c_uint16),
             ("id",           c_uint16),
             ("offset",       c_uint16),
             ("ttl",          c_uint8),
             ("protocol_num", c_uint8),
             ("sum",          c_uint16),
             ("src",          c_uint32),
             ("dst",          c_uint32)]
    
    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}
        
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)
    
    
    
class ICMP(Structure):
    _fields_ = [
    ("type",         c_uint8),
    ("code",         c_uint8),
    ("checksum",     c_uint16),
    ("unused",       c_uint16),
    ("next_hop_mtu", c_int16)
    ]
    
    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer):
        pass
    

if os.name == 'nt':
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP
        
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    
    
    #Linuxの場合、ポート番号0は自動割当になる
sniffer.bind((host, 0))
    
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    #プロミスキャスモードON
if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

class IP(Structure):
    _fields_ = [
             ("ihl",          c_uint8, 4),
             ("version",      c_uint8, 4),
             ("tos",          c_uint8),
             ("len",          c_uint16),
             ("id",           c_uint16),
             ("offset",       c_uint16),
             ("ttl",          c_uint8),
             ("protocol_num", c_uint8),
             ("sum",          c_uint16),
             ("src",          c_uint32),
             ("dst",          c_uint32)]
    
    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}
        
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)
    
    
    
class ICMP(Structure):
    _fields_ = [
    ("type",         c_uint8),
    ("code",         c_uint8),
    ("checksum",     c_uint16),
    ("unused",       c_uint16),
    ("next_hop_mtu", c_int16)
    ]
    
    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer):
        pass
    

if os.name == 'nt':
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP
        
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    
    
    #Linuxの場合、ポート番号0は自動割当になる
sniffer.bind((host, 0))
    
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
    #プロミスキャスモードON
if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    t = threading.Thread(target=udp_sender,args=(subnet,magic_message))
    t.start()
    
    try:
        while True:
            raw_buffer = sniffer.recvfrom(65565)[0]
    
            ip_header = IP(raw_buffer[0:20])
                
            print("Protocol: %s %s -> %s" % (ip_header.protocol, 
                                            ip_header.src_address, ip_header.dst_address))
            if ip_header.protocol == "ICMP":
                
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset:offset + sizeof(ICMP)]
                
                icmp_header = ICMP(buf)
                
                print("ICMP -> Type: %d Code %d" % (icmp_header.type, icmp_header.code))
                
                if icmp_header.code == 3 and icmp_header.type == 3:
                    if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                        if raw_buffer[len(raw_buffer)-len(magic_message):] == magic_message:
                            print("Host Up: %s" % ip_header.src_address)
                
    except KeyboardInterrupt:
        #プロミスキャスモードOFF
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)    