# -*- coding: utf-8 -*-
# @Time : 01/19/2022 16:19
# @Author : wxy
# @File : run.py
# @Software: PyCharm
import sys
import socket
import pandas as pd
from ctypes import c_int32,sizeof,c_double,c_char,c_int64
from ApsimClient import connect_to_remote_server,run_with_changes,read_output,send_string_to_socket, validate_response

PROPERTY_TYPE_INT = 0
PROPERTY_TYPE_DOUBLE = 1
PROPERTY_TYPE_BOOL = 2
PROPERTY_TYPE_DATE = 3
PROPERTY_TYPE_STRING = 4

try:
    sock = connect_to_remote_server("127.0.0.1", 27747)
    print("Connected\n")
except Exception as e:
    print(e)

ACK='ACK'
FIN='FIN'
COMMAND_RUN='RUN'
COMMAND_READ='READ'
# fdno = sock.fileno()
# print(fdno)
# fdno = int(sys.argv[1])
# sock = socket.fromfd(fdno, socket.AF_INET, socket.SOCK_STREAM)
# par = pd.read_csv('workspace/model_input.csv')
# # print(par['parval'][0])
for v in range(100,500):
    changes = [
               {"path":"[Phenology].Vegetative.Target.FixedValue",
                "value": float(v),
               "paramtype": PROPERTY_TYPE_DOUBLE}]
    run_with_changes(sock,changes)
    tablename='Report'
    param_list={
                # 'Year': c_int32,
                'DayOfYear':c_int32,
                'Yield':c_double,
                'Soybean.Phenology.Stage':c_double}
    results=read_output(sock,tablename,param_list)

    df = pd.DataFrame(results)
    print(df)
    # df.to_csv('workspace/model_output.csv',index=None)
    # send_string_to_socket(sock, FIN)

    # validate_response(sock, ACK)
# validate_response(sock, FIN)
# run_with_changes(sock,changes)
# send_string_to_socket(sock, ACK)
# validate_response(socket, ACK)