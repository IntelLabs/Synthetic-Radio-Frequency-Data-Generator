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
n_sym = ctypes.c_int(8)
sps = ctypes.c_int(8)
n_samps = ctypes.c_int(n_sym.value*sps.value)

# channel
snr = ctypes.c_float(5.0)
# fo = ctypes.c_float(-0.1*np.pi)
fo = ctypes.c_float(-0.1)
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
lindemod.linear_demodulate(modtype, order, n_sym, sps, rs_mI, rs_mQ, rs, verbose)
ber.ber(n_sym, bps, s, rs, ber_r, verbose)

plt.figure()

plt.title('Tx Symbols')
plt.plot([i for i in smI], [q for q in smQ], 'ro')
plt.xlabel('I')
plt.ylabel('Q')

if save_plots:
    plt.savefig('./tests/figures/linear_tx_sym_const.png')

plt.figure()

plt.title('Tx Symbols')
plt.plot([i for i in smI], label='I')
plt.plot([q for q in smQ], label='Q')
plt.xlabel('t')
plt.legend()

if save_plots:
    plt.savefig('./tests/figures/linear_tx_sym_iq.png')

plt.figure()

plt.title('Tx Samples')
plt.axhline(0, color='k', linewidth=0.5)
plt.plot([i for i in xI], label='I')
plt.plot([q for q in xQ], label='Q')
plt.xlabel('t')
plt.legend()

if save_plots:
    plt.savefig('./tests/figures/linear_tx_samp.png')

plt.figure()

plt.title('Rx Samples')
plt.axhline(0, color='k', linewidth=0.5)
plt.plot([i for i in yI], label='I')
plt.plot([q for q in yQ], label='Q')
plt.xlabel('t')
plt.legend()

if save_plots:
    plt.savefig('./tests/figures/linear_rx_samp.png')

plt.figure()

plt.title('Rx Symbols')
plt.plot([i for i in rs_mI], [q for q in rs_mQ], 'ro')
plt.xlabel('I')
plt.ylabel('Q')
plt.xlim([-2,2])

if save_plots:
    plt.savefig('./tests/figures/linear_rx_sym_const.png')

plt.figure()

plt.title('Rx Symbols')
plt.plot([i for i in rs_mI], label='I')
plt.plot([q for q in rs_mQ], label='Q')
plt.xlabel('t')
plt.legend()

if save_plots:
    plt.savefig('./tests/figures/linear_rx_sym_iq.png')
else:
    plt.show()
