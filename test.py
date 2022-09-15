# -*- coding: utf-8 -*-
# @Time : 12/20/2021 17:14
# @Author : wxy
# @File : test.py
# @Software: PyCharm
import os
import sys
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
from ApsimClient import connect_to_remote_server,run_with_changes,read_output
import pyemu
sys.path.append(os.path.abspath(os.path.join('..', 'pestpp_exes')))

# pyemu.pst_utils.csv_to_ins_file(csv_filename='workspace/model_output.csv',
#                                 only_cols=['DayOfYear', 'Yield'],
#                                 ins_filename='workspace/model_output.ins',
#                                 includes_index=True)
#
# # para
# # pyemu.utils.pst_from._write_direct_df_tpl(df=para,
# #                                           name='',
# #                                           index_cols=['parname'],
# #                                           use_cols=['parval'],
# #                                           typ='grid',
# #                                           longnames=False,
# #                                           tpl_filename='workspace/model_input.tpl',
# #                                           in_filename='workspace/model_input.csv',
# #                                           )
#
#
tpl_files = ['workspace/model_input.tpl']
in_files = ['workspace/model_input.csv']
ins_files = ['workspace/model_output.ins']
out_files = ['workspace/model_output.csv']

pst = pyemu.Pst.from_io_files(tpl_files, in_files, ins_files, out_files)
#测量数据生成指令文件
pyemu.pst_utils.csv_to_ins_file(csv_filename='workspace/Observation.csv',
                                only_cols=['DayOfYear', 'Yield'],
                                ins_filename='workspace/Observation.ins',
                                includes_index=True)
obf = pyemu.pst_utils.InstructionFile(pst=pst,
                                      ins_filename='workspace/Observation.ins')
obs_df = obf.read_output_file('workspace/Observation.csv')
pst.control_data.pestmode= "estimation"
#----------------------------------------------------
pst.observation_data.obsval = obs_df
pst.observation_data.loc[:,"weight"] = 1.0
pst.observation_data.loc[:,'obgnme'] = 'obsgroup'
pst.parameter_data.loc[:,"partrans"] = "log"
# print(pst.control_data.parse_values_from_lines())
#----------------------------------------------------
pst.parameter_data.loc[:, "parval1"] = 300
pst.parameter_data.loc[:, "parlbnd"] = 200
pst.parameter_data.loc[:, "parubnd"] = 400
# print(pst.parameter_data.columns)
pst.control_data.noptmax = -1

#========================================================
pst.model_command = ["python run.py"]
pst.write("workspace/test.pst")
#-------------------------------------------------------

binpath = r'd:/ApsimClient/pestpp_exes/'
# subprocess.call(binpath+"pestchek workspace/test.pst",cwd='.')
#=======================================================
pyemu.os_utils.run(binpath+"pestpp-glm workspace/test.pst",cwd='.',verbose=False)
# pyemu.helpers.start_workers()