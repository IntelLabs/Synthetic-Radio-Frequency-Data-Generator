#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.abspath("."))

import ctypes
import numpy as np
import matplotlib.pyplot as plt

from utils import mod_int2str as mod_map

save_plots=True

verbose = ctypes.c_int(0)
seed = ctypes.c_int(-1)

## Load C module
mod = ctypes.CDLL(os.path.abspath('./cmodules/modulate'))
tx = ctypes.CDLL(os.path.abspath('./cmodules/rrc_tx'))
chan = ctypes.CDLL(os.path.abspath('./cmodules/channel'))
rx = ctypes.CDLL(os.path.abspath('./cmodules/rrc_rx'))
demod = ctypes.CDLL(os.path.abspath('./cmodules/demodulate'))
ber = ctypes.CDLL(os.path.abspath('./cmodules/ber'))

## Init vars, convert to ctypes
# general
modname = '8psk'
m = mod_map[modname]
modtype = ctypes.c_int(m[0])   
order = ctypes.c_int(m[1])
bps = ctypes.c_int(m[2])
n_sym = ctypes.c_int(10000)
sps = ctypes.c_int(8) 
n_samps = ctypes.c_int(n_sym.value*sps.value)

# filter
delay = ctypes.c_uint(3)
beta = ctypes.c_float(0.35)
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

snr_test = np.arange(0., 20.1, 1)
ber_test = []
for curr in snr_test:
    snr = ctypes.c_float(curr)

    mod.modulate(modtype, order, n_sym, s, smI, smQ, verbose, seed)
    tx.rrc_tx(n_sym, sps, delay, beta, dt, smI, smQ, xI, xQ, verbose)
    chan.channel(snr, n_sym, sps, xI, xQ, yI, yQ, verbose, seed)
    rx.rrc_rx(n_sym, sps, delay, beta, dt, yI, yQ, rs_mI, rs_mQ, verbose)
    demod.demodulate(modtype, order, n_sym, sps, rs_mI, rs_mQ, rs, verbose)
    ber.ber(n_sym, bps, s, rs, ber_r, verbose)
    ber_test.append(ber_r[0])

plt.figure()
plt.plot(snr_test, ber_test, label='simulation')
plt.xlim([snr_test[0], snr_test[-1]])
plt.xlabel('SNR (dB)')
plt.ylim([0.00001, 1])
plt.yscale('log')
plt.ylabel('BER')
plt.title(modname)
plt.grid()

if save_plots:
    plt.savefig('./tests/figures/linear_ber_rrc.png')
else:
    plt.show()
