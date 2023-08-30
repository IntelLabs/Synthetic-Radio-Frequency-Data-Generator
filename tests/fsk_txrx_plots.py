#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.abspath("."))

import ctypes
import numpy as np
import matplotlib.pyplot as plt

from utils import mod_str2int as mod_map
from utils import get_psd

save_plots = True
verbose = ctypes.c_int(0)
seed = ctypes.c_int(-1)

## load c modules
mod = ctypes.CDLL(os.path.abspath("./cmodules/fsk_modulate"))
chan = ctypes.CDLL(os.path.abspath("./cmodules/channel"))
demod = ctypes.CDLL(os.path.abspath("./cmodules/fsk_demodulate"))
ber = ctypes.CDLL(os.path.abspath("./cmodules/ber"))

## init ctypes
m = mod_map['msk']
modtype = ctypes.c_int(m[0])
bps = ctypes.c_int(int(np.log2(m[1])))
modidx = ctypes.c_float(m[2])
pulseshape = ctypes.c_int(m[3])

n_sym = ctypes.c_int(8)
sps = ctypes.c_int(4)
n_samps = ctypes.c_int(n_sym.value*sps.value)

snr = ctypes.c_float(20.0)
fo = ctypes.c_float(0.0*np.pi)
po = ctypes.c_float(0.0*np.pi)

delay = ctypes.c_uint(3)
beta = ctypes.c_float(0.35)
dt = ctypes.c_float(0.0)

## return arrays
ber_r = (ctypes.c_float * 1)(*np.zeros(1))
s = (ctypes.c_uint * n_sym.value)(*np.zeros(n_sym.value, dtype=int))
xI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
xQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
yI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
yQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
rs = (ctypes.c_uint * n_sym.value)(*np.zeros(n_sym.value, dtype=int))

mod.fsk_modulate(n_sym, bps, modidx, pulseshape, sps, delay, beta, s, xI, xQ, verbose, seed)
chan.channel(snr, n_sym, sps, fo, po, xI, xQ, yI, yQ, verbose, seed)
demod.fsk_demodulate(n_sym, bps, modidx, pulseshape, sps, delay, beta, yI, yQ, rs, verbose)

xI = [i for i in xI]
xQ = [q for q in xQ]
yI = [i for i in yI]
yQ = [q for q in yQ]
s = [i for i in s]
rs = [i for i in rs]

## psd
tx_psd = get_psd([i for i in xI], [q for q in xQ], 1024)
rx_psd = get_psd([i for i in yI], [q for q in yQ], 1024)

p = 128

plt.figure()
plt.title('Tx Samples')
plt.plot(xI[:p], label='I')
plt.plot(xQ[:p], label='Q')
plt.xlabel('t')
plt.legend()

if save_plots:
    plt.savefig('./tests/figures/tx_samp.png')

plt.figure()

plt.title('Tx PSD')
plt.plot(tx_psd)

if save_plots:
    plt.savefig('./tests/figures/tx_psd.png')

plt.figure()

plt.title('Rx Samples')
plt.plot(yI[:p], label='I')
plt.plot(yQ[:p], label='Q')
plt.xlabel('t')
plt.legend()

if save_plots:
    plt.savefig('./tests/figures/rx_samp.png')

plt.figure()

plt.title('Rx PSD')
plt.plot(rx_psd)

if save_plots:
    plt.savefig('./tests/figures/rx_psd.png')
else:
    plt.show()
