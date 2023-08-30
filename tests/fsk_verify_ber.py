#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.abspath("."))

import ctypes
import numpy as np
import matplotlib.pyplot as plt

from utils import mod_str2int as mod_map

def get_ber(s, rs, delay):
    s = s[:-delay]
    rs = rs[delay:]
    err = 0
    for i in range(len(s)):
        if s[i] != rs[i]:
            err += 1
    return err/float(len(s))

save_plots = True
verbose = ctypes.c_int(0)
seed = ctypes.c_int(-1)

## load c modules
mod = ctypes.CDLL(os.path.abspath("./cmodules/fsk_modulate"))
chan = ctypes.CDLL(os.path.abspath("./cmodules/channel"))
demod = ctypes.CDLL(os.path.abspath("./cmodules/fsk_demodulate"))
ber = ctypes.CDLL(os.path.abspath("./cmodules/ber"))

## init ctypes
modname = 'msk'
m = mod_map[modname]
modtype = ctypes.c_int(m[0])
bps = ctypes.c_int(int(np.log2(m[1])))
modidx = ctypes.c_float(m[2])
pulseshape = ctypes.c_int(m[3])

n_sym = ctypes.c_int(102400)
sps = ctypes.c_int(8)
n_samps = ctypes.c_int(n_sym.value*sps.value)

fo = ctypes.c_float(0.0*np.pi)
po = ctypes.c_float(0.0*np.pi)

delay = ctypes.c_uint(3)
beta = ctypes.c_float(0.35)
dt = ctypes.c_float(0.0)

## return arrays
s = (ctypes.c_uint * n_sym.value)(*np.zeros(n_sym.value, dtype=int))
xI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
xQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
yI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
yQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
rs = (ctypes.c_uint * n_sym.value)(*np.zeros(n_sym.value, dtype=int))

snr_test = np.arange(0.,20.1, 1)
ber_test = []

for curr in snr_test:
    snr = ctypes.c_float(curr)

    mod.fsk_modulate(n_sym, bps, modidx, pulseshape, sps, delay, beta, s, xI, xQ, verbose, seed)
    chan.channel(snr, n_sym, sps, fo, po, xI, xQ, yI, yQ, verbose, seed)
    demod.fsk_demodulate(n_sym, bps, modidx, pulseshape, sps, delay, beta, yI, yQ, rs, verbose)
    if modname == 'msk':
        ber_test.append(get_ber([i for i in s], [i for i in rs], delay.value+1))
    elif modname == 'gmsk':
        ber_test.append(get_ber([i for i in s], [i for i in rs], (2*delay.value)+1))

plt.figure()
plt.plot(snr_test, ber_test, label='simulation')
plt.xlim([snr_test[0], snr_test[-1]])
plt.xlabel('SNR (dB)')
plt.ylim([0.00001, 1])
plt.yscale('log')
plt.ylabel('BER')
plt.title(modname)
plt.grid()
plt.legend()

if save_plots:
    plt.savefig('./tests/figures/fsk_ber.png')
else:
    plt.show()