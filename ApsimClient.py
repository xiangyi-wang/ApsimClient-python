# -*- coding: utf-8 -*-
# @Time : 10/20/2021 14:54
# @Author : wxy
# @File : ApsimClient.py
# @Software: PyCharm
import os.path
import sys
import random
from ctypes import c_int32,sizeof,c_double,c_char,c_int64
import struct
import socket
import platform
import subprocess
from time import sleep
import pandas as pd
# from subprocess import Popen
ACK='ACK'
FIN='FIN'
COMMAND_RUN='RUN'
COMMAND_READ='READ'
PROPERTY_TYPE_INT = 0
PROPERTY_TYPE_DOUBLE = 1
PROPERTY_TYPE_BOOL = 2
PROPERTY_TYPE_DATE = 3
PROPERTY_TYPE_STRING = 4
# PROPERTY_TYPE_INT_ARRAY = 5
# PROPERTY_TYPE_DOUBLE_ARRAY = 6
# PROPERTY_TYPE_BOOL_ARRAY = 7
# PROPERTY_TYPE_DATE_ARRAY = 8
# PROPERTY_TYPE_STRING_ARRAY = 9
def connect_to_remote_server(ip_address, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip_address, port))
    except:
        pass
    return client
def connect_to_local_server(pipe_name):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect("\0" + pipe_name)
    except:
        pass
    return client
def disconnect_from_server(socket):
    socket.close()
def send_to_socket(socket,msg,slen):

    if isinstance (msg,int):
        msg = struct.pack('@i', msg)
    elif isinstance (msg,float):
        msg = struct.pack('@d', msg)
    elif isinstance(msg, str):
        msg = struct.pack('@'+str(slen)+'s',msg.encode())

    slen = struct.pack('i',slen)
    # Send message length.
    socket.send(slen)
    # Send the message itself
    socket.send(msg)

def send_string_to_socket(socket,msg):

    # length = len(msg.encode())
    # slen = '%08d' % length
    # socket.sendall(msg.encode())
    send_to_socket(socket, msg, len(msg))
def read_from_socket(socket):
    # 解析header
    header = socket.recv(4)
    total_size = struct.unpack('i', header)[0]
    recv_size = 0
    recv_data = b''
    while recv_size < total_size:
        data = socket.recv(1024)
        recv_size += len(data)
        recv_data += data

    return recv_size,recv_data

def validate_response(socket,expected):

    data_size,data = read_from_socket(socket)
    resp = data.decode("utf-8")

    assert resp == expected, "Expected response '%s' but got '%s'\n"%(expected, resp)

def send_replacement_to_socket(socket,change):

    # 1. Send parameter path.
    send_string_to_socket(socket, change["path"])
    validate_response(socket, ACK)
    # 2. Send parameter type.
    send_to_socket(socket, change["paramtype"], sizeof(c_int32))
    validate_response(socket, ACK)
    # 3. Send the parameter itself.
    if isinstance(change["value"],float):
        typeofvalue = c_double
        send_to_socket(socket, change["value"], sizeof(typeofvalue))
    elif isinstance(change["value"],int):
        typeofvalue = c_int32
        send_to_socket(socket, change["value"], sizeof(typeofvalue))
    elif isinstance(change["value"],str):
        send_string_to_socket(socket, change["value"])

    validate_response(socket, ACK)
def run_with_changes(socket,changes):
    send_string_to_socket(socket, COMMAND_RUN)
    validate_response(socket, ACK)

    for i in range(len(changes)):
        send_replacement_to_socket(socket, changes[i])

    send_string_to_socket(socket, FIN)
    validate_response(socket, ACK)
    validate_response(socket, FIN)
    print('Run Finished')

def read_output(socket,tablename,param_list):
    # 1. Send READ command.
    send_string_to_socket(socket, COMMAND_READ)
    # 2. Receive ACK-> validate server received read commond
    validate_response(socket, ACK)
    # 3. Send table name.
    send_string_to_socket(socket, tablename)
    # 4. Receive ACK-> validate server received table name
    validate_response(socket, ACK)
    # 5. Send parameter names one at a time.
    for param_name in param_list:
        send_string_to_socket(socket, param_name)
        # Should receive ACK after each message.
        validate_response(socket, ACK)  #
    # Send FIN to indicate end of parameter names.
    send_string_to_socket(socket, FIN)
    send_string_to_socket(socket, ACK)

    results={}
    for param_name,param_type in param_list.items():
        result_output_of_one = read_output_of_one(socket, param_type)
        results[param_name]=result_output_of_one
        send_string_to_socket(socket, ACK)

    validate_response(socket, ACK)#这里注意
    disconnect_from_server(socket)
    return results

def read_output_of_one(socket,param_type):
    recv_size , recv_data = read_from_socket(socket)
    # print(recv_data)
    # print(recv_size)
    if param_type==c_int32:
        # result_of_one = result_of_one.decode()
        result_of_one = struct.unpack('@i', recv_data)[0]
    elif param_type==c_double:
        result_of_one = struct.unpack('@d', recv_data)[0]
    elif param_type==c_char:
        # result_of_one = struct.unpack('@s', recv_data)[0]
        result_of_one = recv_data.decode("utf-8")
    # print(result_of_one)
    # result_of_all = []
    # for i in range(0, recv_size, sizeof(param_type)):
    #     result_of_one = recv_data[i:i + sizeof(param_type)]
    #     # print(result_of_one)
    #     if param_type==c_int32:
    #         # result_of_one = result_of_one.decode()
    #         result_of_one = struct.unpack('@i', result_of_one)[0]
    #     elif param_type==c_double:
    #         result_of_one = struct.unpack('@d', result_of_one)[0]
    #     elif param_type==c_char:
    #         # result_of_one = struct.unpack('@s', result_of_one)[0]
    #         result_of_one = result_of_one.decode("utf-8")
    #     # print(result_of_one)
    #     result_of_all.append(result_of_one)

    return result_of_one
    # clientSoscket.close()
def start_apsim_server(SERVER_PATH,JSON_PATH,JSON_NAME,HOST='0.0.0.0',PORT=27747,SOCKETNAME='ApsimNGServer'):
   # COMMOND_LINE = SERVER_PATH+'/apsim-server.exe'          \
   #                  +' --file ' + JSON_PATH+'/'+JSON_NAME  \
   #                  +' --verbose '                         \
   #                  +' --keep-alive '                      \
   #                  +' --native '                          \
   #                  +' --remote '                          \
   #                  +' --address ' + HOST                  \
   #                  +' --port ' + str(PORT)
   # subprocess.check_call(COMMOND_LINE, shell=False, cwd=JSON_PATH)
   # subprocess.Popen(COMMOND_LINE)
   subprocess.Popen([SERVER_PATH+'/apsim-server.exe',
                  '--file',JSON_PATH+'/'+JSON_NAME, # Required. .apsimx file to hold in memory.
                  '--verbose',                      # Display verbose debugging info
                  '--keep-alive',                   # Keep the server alive after client disconnects
                  '--native',                       # Expect communications from a native client
                  '--remote',                       # Expect connections from a remote client
                  '--address',HOST,                 # (Default: 0.0.0.0) IP Address on which to listen for connections. Only used when accepting
                                                    # connections over network
                  '--port', str(PORT),              # (Default: 27746) Port number on which to listen for connections. Only used when accepting
                                                    # connections over network
                  '--socket-name',SOCKETNAME] ,     # (Default: ApsimNGServer) Socket name. Only used when running in local mode (--local)
                  cwd=JSON_PATH)
   sleep(3)


if __name__ == '__main__':
    SERVER_PATH=r'E:/Apsim/bin/'
    JSON_PATH=r'E:/Apsim/Examples'
    JSON_NAME='aaa.apsimx'
    # start_apsim_server(SERVER_PATH,JSON_PATH,JSON_NAME,PORT=27747)

    #C:\Users\admin>E:\APSIM\bin/apsim-server.exe --file E:\APSIM\Examples\Wheat.apsimx --verbose --native --remote --keep-alive --address 127.0.0.1 --port 27747
    # Connect to the socket.
    print("Connecting to server...")
    try:
        sock = connect_to_remote_server("127.0.0.1", 27747)
        print("Connected\n")
    except Exception as e:
        print(e)

    changes=[

        {"path": "[Rua].Command[3]",
         "value": '[Structure].Phyllochron.Phyllochron.Phyllochron.XYPairs.X = 0,0.15,0.74,0.75,1',
         'paramtype': PROPERTY_TYPE_STRING
         },

    ]
    run_with_changes(sock,changes)
    tablename='Report'
    param_list={
                'Clock.Today.DayOfYear':c_int32,
                'Yield':c_double}
    results=read_output(sock,tablename,param_list)
    print(results)

