# -*- coding: utf-8 -*-
# @Time : 10/20/2021 14:54
# @Author : wxy
# @File : ApsimClient.py
# @Software: PyCharm
import os.path
import sys
from ctypes import c_int32,sizeof,c_double,c_char,c_int64
import struct
import socket
import platform
import subprocess
from time import sleep
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
PROPERTY_TYPE_INT_ARRAY = 5
PROPERTY_TYPE_DOUBLE_ARRAY = 6
PROPERTY_TYPE_BOOL_ARRAY = 7
PROPERTY_TYPE_DATE_ARRAY = 8
PROPERTY_TYPE_STRING_ARRAY = 9
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
    # slen = struct.pack('@'+str(len(str(slen)))+'s',str(slen).encode())
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

def read_from_socket(socket,slen):
    #Read message length (4 bytes)
    header = socket.recv(4)
    header = struct.unpack('i', header)
    # data_size
    # Read n bytes
    servermsg = socket.recv(slen)
    data =servermsg.decode("utf-8")
    # data = (struct.unpack('@'+str(data_size)+'s',servermsg)[0]).decode()
    # print(data_size,data)
    return header,data
def validate_response(socket,expected):
    data_size,data = read_from_socket(socket, slen=4)
    # print(data)
    if data!= expected:
        if expected=='FIN':
            resp = socket.recv(data_size[0]-4)
            resp = resp.decode("utf-8")
            resp_all=data+resp
        else:
            resp_all=data
        assert data == expected, "Expected response '%s' but got '%s'\n"%(expected, resp_all)

def send_replacement_to_socket(socket,change):

    # 1. Send parameter path.
    send_string_to_socket(socket, change["path"])
    validate_response(socket, ACK)
    # 2. Send parameter type.
    send_to_socket(socket, change["paramtype"], sizeof(c_int32))
    validate_response(socket, ACK)
    # 3. Send the parameter itself.
    send_to_socket(socket, change["value"], sizeof(c_double))
    validate_response(socket, ACK)
def run_with_changes(socket,changes):
    send_string_to_socket(socket, COMMAND_RUN)
    validate_response(socket, ACK)

    for i in range(len(changes)):
        send_replacement_to_socket(socket, changes[i])

    send_string_to_socket(socket, FIN)
    validate_response(socket, ACK)
    validate_response(socket, FIN)
    print('run finished')

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
    validate_response(socket, FIN)
    results={}

    for param_name,param_type in param_list.items():
        result_output_of_one = read_output_of_one(socket, param_type)
        results[param_name]=result_output_of_one
        send_string_to_socket(socket, ACK)
    # validate_response(socket, ACK)
    return results
def read_output_of_one(socket,param_type):
    # 解析header
    header = socket.recv(4)
    total_size = struct.unpack('i', header)[0]
    # print(total_size)
    recv_data = socket.recv(total_size)

    # recv_size = 0
    # recv_data = ''
    # while recv_size < total_size:
    #     recv_data = socket.recv(total_size)
    #     recv_size += len(recv_data)
    #     recv_data += recv_data
    #     print(recv_data)

    result_of_all = []
    for i in range(0, total_size, sizeof(param_type)):
        result_of_one = recv_data[i:i + sizeof(param_type)]
        # print(result_of_one)
        if param_type==c_int32:
            # result_of_one = result_of_one.decode()
            result_of_one = struct.unpack('@i', result_of_one)[0]
        elif param_type==c_double:
            result_of_one = struct.unpack('@d', result_of_one)[0]
        elif param_type==c_char:
            result_of_one = struct.unpack('@s', result_of_one)[0]
        result_of_all.append(result_of_one)

    return result_of_all
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
    SERVER_PATH=r'E:\Apsim\bin/'
    JSON_PATH=r'E:\Apsim\Examples'
    JSON_NAME='Wheat.apsimx'
    # start_apsim_server(SERVER_PATH,JSON_PATH,JSON_NAME,PORT=27747)
    # data='[Phenology].Phyllochron.BasePhyllochron.FixedValue = 1.5'
    # start_apsim_client(msg=data,port=27747)
    #C:\Users\admin>E:\APSIM\bin/apsim-server.exe --file E:\APSIM\Examples\Wheat.apsimx --verbose --native --remote --keep-alive --address 127.0.0.1 --port 27747
    # Connect to the socket.
    print("Connecting to server...")
    sock = connect_to_remote_server("127.0.0.1", 27747)
    print("connected\n")
    changes=[
        {"path":"[Phenology].Phyllochron.BasePhyllochron.FixedValue",
         "value":1.5,
         'paramtype':PROPERTY_TYPE_DOUBLE
         }]
    run_with_changes(sock,changes)
    tablename='Report'
    # param_list=['Clock.Today.DayOfYear','Yield']#'Clock.Today',
    # nparams=len(param_list)
    # args = {'tablename':'Report','params':{'name':['Yield'],'length':[sizeof(c_double)]}}
    param_list={'Clock.Today.DayOfYear':c_int32,
                'Yield':c_double}
    results=read_output(sock,tablename,param_list)
    print(results)

