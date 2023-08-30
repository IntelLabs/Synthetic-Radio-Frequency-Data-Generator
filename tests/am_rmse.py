#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.abspath("."))

import ctypes
import numpy as np
import matplotlib.pyplot as plt

from utils import mod_str2int as mod_map

save_plots = True
verbose = ctypes.c_int(0)
seed = ctypes.c_int(-1)

## Load C module
cam_m = ctypes.CDLL(os.path.abspath("./cmodules/am_modulate"))
chan = ctypes.CDLL(os.path.abspath('./cmodules/channel'))
cam_d = ctypes.CDLL(os.path.abspath("./cmodules/am_demodulate"))
crmse = ctypes.CDLL(os.path.abspath("./cmodules/rmse"))

## Init vars, convert to ctypes
# general
modname = 'usb'
m = mod_map[modname][0]
n_samps = ctypes.c_int(2500)

# channel
fo = ctypes.c_float(0.05*np.pi)
po = ctypes.c_float(0.0*np.pi)

mod_idx = ctypes.c_float(0.9)
sps = ctypes.c_int(1)

## create return arrays
x = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
xI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
xQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
yI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
yQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
y = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
rmse_r = (ctypes.c_float * 1)(*np.zeros(1))
delay_r = (ctypes.c_uint * 1)(*np.zeros(1, dtype=int))

snr_test = np.arange(0., 30.1, 1)
rmse_test = []

for curr in snr_test:
    snr = ctypes.c_float(curr)

    ## calls to c code
    cam_m.am_modulate(m, mod_idx, n_samps, x, xI, xQ, verbose, seed)
    chan.channel(snr, n_samps, sps, fo, po, xI, xQ, yI, yQ, verbose, seed)
    cam_d.am_demodulate(m, mod_idx, n_samps, yI, yQ, y, delay_r,  verbose)
    crmse.rmse(n_samps, ctypes.c_uint(delay_r[0]), x, y, rmse_r, verbose)
    rmse_test.append(rmse_r[0])

plt.figure()
plt.plot(snr_test, rmse_test)
plt.xlim([snr_test[0], snr_test[-1]])
plt.xlabel('SNR (dB)')
plt.ylabel('RMSE')
plt.title(modname)
plt.grid()

if save_plots:
    plt.savefig('./tests/figures/am_rmse.png')
else:
    plt.show()