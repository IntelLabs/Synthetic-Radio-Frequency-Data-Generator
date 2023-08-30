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
linmod = ctypes.CDLL(os.path.abspath("./cmodules/linear_modulate"))
tx = ctypes.CDLL(os.path.abspath('./cmodules/rrc_tx'))
chan = ctypes.CDLL(os.path.abspath('./cmodules/channel'))
rx = ctypes.CDLL(os.path.abspath('./cmodules/rrc_rx'))
lindemod = ctypes.CDLL(os.path.abspath('./cmodules/linear_demodulate'))
ber = ctypes.CDLL(os.path.abspath('./cmodules/ber'))

## Init vars, convert to ctypes
# general
m = mod_map['qpsk']
modtype = ctypes.c_int(m[0])   ## 0 for PSK, 1 for QAM
order = ctypes.c_int(m[1])
bps = ctypes.c_int(m[2])
n_sym = ctypes.c_int(1024)
sps = ctypes.c_int(8)
n_samps = ctypes.c_int(n_sym.value*sps.value)

# channel
snr = ctypes.c_float(10.0)
fo = ctypes.c_float(-0.1*np.pi)
po = ctypes.c_float(0.0)

# filter
delay = ctypes.c_uint(3)
beta = ctypes.c_float(.35)
dt = ctypes.c_float(0.)

## return arrays
ber_r = (ctypes.c_float * 1)(*np.zeros(1))
s = (ctypes.c_uint * n_sym.value)(*np.zeros(n_sym.value, dtype=int))
smI = (ctypes.c_float * n_sym.value)(*np.zeros(n_sym.value))
smQ = (ctypes.c_float * n_sym.value)(*np.zeros(n_sym.value))
xI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
xQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
yI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
yQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
rs_mI = (ctypes.c_float * n_sym.value)(*np.zeros(n_sym.value))
rs_mQ = (ctypes.c_float * n_sym.value)(*np.zeros(n_sym.value))
rs = (ctypes.c_uint * n_sym.value)(*np.zeros(n_sym.value, dtype=int))

## Use liquid to generate some samples
## returns rI, rQ of length n_samps
linmod.linear_modulate(modtype, order, n_sym, s, smI, smQ, verbose, seed)
tx.rrc_tx(n_sym, sps, delay, beta, dt, smI, smQ, xI, xQ, verbose)
chan.channel(snr, n_sym, sps, fo, po, xI, xQ, yI, yQ, verbose, seed)
rx.rrc_rx(n_sym, sps, delay, beta, dt, yI, yQ, rs_mI, rs_mQ, verbose)

yI = [i for i in yI]
yQ = [1j*q for q in yQ]
yIQ = np.array([yI[i]+yQ[i] for i in range(len(yI))])

# fy = np.fft.fft(yIQ, 1024)
fy, _ = plt.psd(yIQ)
fy = 10*np.log10(fy)
# l = int(len(fy)/2)
# fy = np.hstack((fy[l:], fy[:l]))

plt.plot(fy)
plt.ylim(10*np.log10(1),10*np.log10(20))
if save_plots:
    plt.savefig('./tests/figures/linear_fft.png')