#!/usr/bin/python3

import os
import sys
sys.path.append(os.path.abspath("."))

import ctypes
import numpy as np
import matplotlib.pyplot as plt

from utils import mod_str2int as mod_map

verbose = ctypes.c_int(0)
seed = ctypes.c_int(-1)
save_plots = True

## theoretical ber curves
## calculated using MATLAB berawgn
theory = {'bpsk':[0.07865, 0.056282, 0.037506, 0.022878, 0.012501, 0.0059539, 0.0023883, 0.00077267, 0.00019091,
                  3.3627e-05, 3.8721e-06, 2.6131e-07, 9.006e-09, 1.3329e-10, 6.8102e-13, 9.124e-16, 2.2674e-19,
                  6.759e-24, 1.396e-29, 1.0011e-36, 1.0442e-45],
          'qpsk':[0.15866, 0.13093, 0.10403, 0.078896, 0.056495, 0.037679, 0.023007, 0.012587, 0.0060044,
                  0.0024133, 0.0007827, 0.00019399, 3.4303e-05, 3.9692e-06, 2.6951e-07, 9.361e-09, 1.399e-09,
                  7.236e-13, 9.845e-16, 2.4945e-19, 7.6199e-24],
          '8psk':[0.24115, 0.21586, 0.19029, 0.16504, 0.14064, 0.11754, 0.09025, 0.076242, 0.058318, 0.042467,
                  0.029013, 0.018277, 0.010399, 0.0052101, 0.0022266, 0.00077982, 0.00021283, 4.2476e-05, 
                  5.7223e-06, 4.704e-07, 2.0779e-08],
          '16qam':[0.28728, 0.26248, 0.23723, 0.21216, 0.18774, 0.16417, 0.14144, 0.11944, 0.098171, 0.077858,
                   0.058993, 0.042212, 0.02813, 0.017159, 0.0093756, 0.0044654, 0.0017912, 0.00057951, 0.00014318,
                   2.522e-05, 2.9041e-06],
          '64qam':[0.35986, 0.34279, 0.32447, 0.30492, 0.28421, 0.26251, 0.2401, 0.21743, 0.19498, 0.17324, 
                   0.15255, 0.13302, 0.11458, 0.097022, 0.080203, 0.064159, 0.049171, 0.035695, 0.024217,
                   0.015106, 0.0084864]}

## Load C module
mod = ctypes.CDLL(os.path.abspath('./cmodules/linear_modulate'))
tx = ctypes.CDLL(os.path.abspath('./cmodules/rrc_tx'))
chan = ctypes.CDLL(os.path.abspath('./cmodules/channel'))
rx = ctypes.CDLL(os.path.abspath('./cmodules/rrc_rx'))
demod = ctypes.CDLL(os.path.abspath('./cmodules/linear_demodulate'))
ber = ctypes.CDLL(os.path.abspath('./cmodules/ber'))

## Init vars, convert to ctypes
# general
modname = 'qpsk'
m = mod_map[modname]
t = theory[modname]
modtype = ctypes.c_int(m[0])   
order = ctypes.c_int(m[1])
bps = ctypes.c_int(m[2])
n_sym = ctypes.c_int(100000)
sps = ctypes.c_int(1) ## to bypass rrc
fo = ctypes.c_float(0.0*np.pi)
po = ctypes.c_float(0.0)

## return arrays
ber_r = (ctypes.c_float * 1)(*np.zeros(1))
s = (ctypes.c_uint * n_sym.value)(*np.zeros(n_sym.value, dtype=int))
smI = (ctypes.c_float * n_sym.value)(*np.zeros(n_sym.value))
smQ = (ctypes.c_float * n_sym.value)(*np.zeros(n_sym.value))
rs_mI = (ctypes.c_float * n_sym.value)(*np.zeros(n_sym.value))
rs_mQ = (ctypes.c_float * n_sym.value)(*np.zeros(n_sym.value))
rs = (ctypes.c_uint * n_sym.value)(*np.zeros(n_sym.value, dtype=int))

snr_test = np.arange(0., 20.1, 1)
ber_test = []
for curr in snr_test:
    snr = ctypes.c_float(curr)
    seed = ctypes.c_int(np.random.randint(1e9))

    mod.linear_modulate(modtype, order, n_sym, s, smI, smQ, verbose, seed)
    chan.channel(snr, n_sym, sps, fo, po, smI, smQ, rs_mI, rs_mQ, verbose, seed)
    demod.linear_demodulate(modtype, order, n_sym, sps, rs_mI, rs_mQ, rs, verbose)
    ber.ber(n_sym, bps, s, rs, ber_r, verbose)
    ber_test.append(ber_r[0])

plt.figure()
plt.plot(snr_test, ber_test, label='simulation')
plt.plot(snr_test, t, label='theory')
plt.xlim([snr_test[0], snr_test[-1]])
plt.xlabel('SNR (dB)')
plt.ylim([0.00001, 1])
plt.yscale('log')
plt.ylabel('BER')
plt.title(modname)
plt.grid()
plt.legend()

if save_plots:
    plt.savefig('./tests/figures/linear_ber.png')
else:
    plt.show()
