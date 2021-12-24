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
import pyemu
import numpy as np
sys.path.append(os.path.abspath(os.path.join('..', 'pestpp_exes/bin')))
template_ws = "template"
tmp_model_ws = "temp_pst_from"

pyemu.pst_utils.csv_to_ins_file(csv_filename='workspacemodel_output.csv',
                                ins_filename='model_output.ins',
                                includes_index=False)
df = pd.read_csv('model_input.csv')

pyemu.utils.pst_from._write_direct_df_tpl(df=df,
                                          name='',
                                          index_cols=['parname'],
                                          use_cols=['parval'],
                                          typ='grid',
                                          longnames=False,
                                          tpl_filename='model_input.tpl',
                                          in_filename='model_input.csv',
                                          )
pf = pyemu.Pst.from_io_files(tpl_files=['model_input.tpl'],
                             in_files=['model_input.csv'],
                             ins_files=['model_output.ins'],
                             out_files=['model_output.csv'],
                             pst_filename='test.pst',
                             pst_path='workspace')