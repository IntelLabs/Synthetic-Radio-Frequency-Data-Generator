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
m = mod_map['usb'][0]
n_samps = ctypes.c_int(500)

# channel
snr = ctypes.c_float(20.0)
fo = ctypes.c_float(0.0*np.pi)
po = ctypes.c_float(0.0*np.pi)

mod_idx = ctypes.c_float(0.8)
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

## calls to c code
cam_m.am_modulate(m, mod_idx, n_samps, x, xI, xQ, verbose, seed)
chan.channel(snr, n_samps, sps, fo, po, xI, xQ, yI, yQ, verbose, seed)
cam_d.am_demodulate(m, mod_idx, n_samps, yI, yQ, y, delay_r, verbose)

plt.figure()

plt.title('Tx Signal')
plt.plot([i for i in x])
plt.xlabel('t')

if save_plots:
    plt.savefig('./tests/figures/am_tx_sig.png')

plt.figure()

plt.title('Tx Samples')
plt.plot([i for i in xI], label='I')
plt.plot([q for q in xQ], label='Q')
plt.xlabel('t')
plt.legend()

if save_plots:
    plt.savefig('./tests/figures/am_tx_samp.png')

plt.figure()

plt.title('Rx Samples')
plt.plot([i for i in yI], label='I')
plt.plot([q for q in yQ], label='Q')
plt.xlabel('t')
plt.legend()

if save_plots:
    plt.savefig('./tests/figures/am_rx_samp.png')

plt.figure()

plt.title('Rx Signal')
plt.plot([i for i in y])
plt.xlabel('t')

if save_plots:
    plt.savefig('./tests/figures/am_rx_sig.png')
else:
    plt.show()
