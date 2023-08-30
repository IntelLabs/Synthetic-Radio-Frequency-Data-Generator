#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.abspath("."))

import json
import ctypes
import numpy as np
import matplotlib.pyplot as plt

from utils import mod_str2int as mod_map

save_plots = True
verbose = ctypes.c_int(0)
seed = ctypes.c_int(-1)

idx = 0
example_len=512
dataset_path = '/store/nosnap/data/example/'

rrc = ctypes.CDLL(os.path.abspath('./cmodules/rrc_rx'))
linear = ctypes.CDLL(os.path.abspath('./cmodules/linear_demodulate'))
am = ctypes.CDLL(os.path.abspath('./cmodules/am_demodulate'))
fm = ctypes.CDLL(os.path.abspath('./cmodules/fm_demodulate'))
fsk = ctypes.CDLL(os.path.abspath('./cmodules/fsk_demodulate'))

files = os.listdir(dataset_path)    # both data and meta files
files = [os.path.join(dataset_path, f.split(".")[0]) for f in files] # add path
files = list(set(files))

for i in range(len(files)):
    f = files[i]

    ## get meta
    with open(f + ".sigmf-meta") as _f:
        f_meta = json.load(_f)

    capture_start = f_meta["captures"][0]["core:sample_start"]
    capture_len = f_meta["captures"][0]["core:length"]

    f_meta = f_meta["annotations"][0] 

    ## get data
    with open(f + ".sigmf-data", 'rb') as _f:
        f_data = np.load(_f)
    I = f_data[capture_start*2 : (example_len+capture_start)*2 : 2]
    Q = f_data[(capture_start*2)+1 : ((example_len+capture_start)*2)+1 : 2]
    modscheme = f_meta["rfml_labels"]["modclass"]


    plt.figure()
    plt.title("Rx Samples")
    plt.plot(I, label='I')
    plt.plot(Q, label='Q')
    plt.xlabel('t')
    plt.legend()

    if save_plots:
        plt.savefig('./tests/figures/dataset/'+modscheme+'.png')




