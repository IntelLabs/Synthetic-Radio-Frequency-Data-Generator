#!/usr/bin/python3

## python imports
import argparse
import json
import numpy as np
import os
from datetime import datetime
import ctypes
import sys

## internal imports
from utils import *

buf = 1024 
halfbuf = 512

## load c modules
clinear = ctypes.CDLL(os.path.abspath("./cmodules/linear_modulate"))
cam = ctypes.CDLL(os.path.abspath("./cmodules/am_modulate"))
cfm = ctypes.CDLL(os.path.abspath("./cmodules/fm_modulate"))
cfsk = ctypes.CDLL(os.path.abspath("./cmodules/fsk_modulate"))
ctx = ctypes.CDLL(os.path.abspath("./cmodules/rrc_tx"))
cchan = ctypes.CDLL(os.path.abspath("./cmodules/channel"))


def generate_linear(idx_start, mod, config):
    verbose = ctypes.c_int(config["verbose"])
    modtype = ctypes.c_int(mod[0])
    n_samps = ctypes.c_int(config["n_samps"]+buf)
    
    sig_params = [(_sps, _beta, _delay, _dt) for _sps in config["symbol_rate"] for _beta in config["rrc_filter"]["beta"] for _delay in config["rrc_filter"]["delay"] for _dt in config["rrc_filter"]["dt"]]
    idx = np.random.choice(len(sig_params), config["n_captures"])
    sig_params = [sig_params[_idx] for _idx in idx]
    idx = np.random.choice(len(config["channel_params"]), config["n_captures"])
    channel_params = [config["channel_params"][_idx] for _idx in idx]

    for i in range(0, config["n_captures"]):
        seed = ctypes.c_int(np.random.randint(1e9))
        snr = ctypes.c_float(channel_params[i][0])
        fo = ctypes.c_float(2.*channel_params[i][1]*np.pi)
        po = ctypes.c_float(channel_params[i][2]) 

        order = ctypes.c_int(mod[1])
        sps = ctypes.c_int(sig_params[i][0])
        n_sym = n_sym = ctypes.c_int(int(np.ceil(n_samps.value/sps.value)))
        beta = ctypes.c_float(sig_params[i][1])
        delay = ctypes.c_uint(int(sig_params[i][2]))
        dt = ctypes.c_float(sig_params[i][3])

        ## create return arrays
        s = (ctypes.c_uint * n_sym.value)(*np.zeros(n_sym.value, dtype=int))
        smI = (ctypes.c_float * n_sym.value)(*np.zeros(n_sym.value))
        smQ = (ctypes.c_float * n_sym.value)(*np.zeros(n_sym.value))
        xI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        xQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        yI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        yQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        clinear.linear_modulate(modtype, order, n_sym, s, smI, smQ, verbose, seed)
        ctx.rrc_tx(n_sym, sps, delay, beta, dt, smI, smQ, xI, xQ, verbose)
        cchan.channel(snr, n_sym, sps, fo, po, xI, xQ, yI, yQ, verbose, seed)

        metadata = {"modname":mod[-1],
                    "modclass":modtype.value,
                    "order":order.value,
                    "n_samps":n_samps.value-buf,
                    "channel_type":config["channel_type"],
                    "snr":snr.value,
                    "filter_type":"rrc",
                    "sps":sps.value,
                    "delay":delay.value,
                    "beta":beta.value,
                    "dt":dt.value,
                    "fo":fo.value,
                    "po":po.value,
                    "savepath":config["savepath"],
                    "savename":config["savename"]}
        
        ## convert to numpy arrays
        I = np.array([_i for _i in yI])
        I = I[halfbuf:-halfbuf]
        Q = np.array([_q for _q in yQ])
        Q = Q[halfbuf:-halfbuf]

        ## save record in sigmf format
        save_sigmf(I, Q, metadata, idx_start+i)

    return idx_start+i+1

def generate_am(idx_start, mod, config):
    verbose = ctypes.c_int(config["verbose"])
    modtype = ctypes.c_int(mod[0])
    n_samps = ctypes.c_int(config["n_samps"]+buf)

    sig_params = config["am_defaults"]["modulation_index"]
    idx = np.random.choice(len(sig_params), config["n_captures"])
    sig_params = [sig_params[_idx] for _idx in idx]
    idx = np.random.choice(len(config["channel_params"]), config["n_captures"])
    channel_params = [config["channel_params"][_idx] for _idx in idx]

    for i in range(0, config["n_captures"]):
        seed = ctypes.c_int(np.random.randint(1e9))
        snr = ctypes.c_float(channel_params[i][0])
        fo = ctypes.c_float(2.*channel_params[i][1]*np.pi)
        po = ctypes.c_float(channel_params[i][2])

        modtype = ctypes.c_int(mod[1])
        mod_idx = ctypes.c_float(sig_params[i])
        sps = ctypes.c_int(1)

        ## create return arrays
        x = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        xI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        xQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        yI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        yQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        
        ## calls to c code
        cam.am_modulate(modtype, mod_idx, n_samps, x, xI, xQ, verbose, seed)
        cchan.channel(snr, n_samps, sps, fo, po, xI, xQ, yI, yQ, verbose, seed)

        metadata = {"modname":mod[-1],
                    "modclass":mod[0],
                    "modvariant":mod[1],
                    "mod_idx":mod_idx.value,
                    "n_samps":n_samps.value-buf,
                    "channel_type":config["channel_type"],
                    "snr":snr.value,
                    "fo":fo.value,
                    "po":po.value,
                    "savepath":config["savepath"],
                    "savename":config["savename"]}
        
        ## convert to numpy arrays
        I = np.array([_i for _i in yI])
        I = I[halfbuf:-halfbuf]
        Q = np.array([_q for _q in yQ])
        Q = Q[halfbuf:-halfbuf]

        ## save record in sigmf format
        save_sigmf(I, Q, metadata, idx_start+i)

    return idx_start+i+1

def generate_fm(idx_start, mod, config):
    verbose = ctypes.c_int(config["verbose"])
    modtype = ctypes.c_int(mod[0])
    n_samps = ctypes.c_int(config["n_samps"]+buf)

    if mod[1] == 0:
        ## narrowband
        sig_params = config["fmnb_defaults"]["modulation_factor"]
    elif mod[1] == 1:
        ## wideband
        sig_params = config["fmwb_defaults"]["modulation_factor"]
    idx = np.random.choice(len(sig_params), config["n_captures"])
    sig_params = [sig_params[_idx] for _idx in idx]
    idx = np.random.choice(len(config["channel_params"]), config["n_captures"])
    channel_params = [config["channel_params"][_idx] for _idx in idx]

    for i in range(0, config["n_captures"]):
        seed = ctypes.c_int(np.random.randint(1e9))

        mod_factor = ctypes.c_float(sig_params[i])

        snr = ctypes.c_float(channel_params[i][0])
        fo = ctypes.c_float(2.*channel_params[i][1]*np.pi)
        po = ctypes.c_float(channel_params[i][2]) 

        sps = ctypes.c_int(1)

        ## create return arrays
        x = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        xI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        xQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        yI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        yQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        
        ## calls to c code
        cfm.fm_modulate(mod_factor, n_samps, x, xI, xQ, verbose, seed)
        cchan.channel(snr, n_samps, sps, fo, po, xI, xQ, yI, yQ, verbose, seed)

        metadata = {"modname":mod[-1],
                    "modclass":mod[0],
                    "modvariant":mod[1],
                    "mod_factor":mod_factor.value,
                    "n_samps":n_samps.value-buf,
                    "channel_type":config["channel_type"],
                    "snr":snr.value,
                    "fo":fo.value,
                    "po":po.value,
                    "savepath":config["savepath"],
                    "savename":config["savename"]}

        ## convert to numpy arrays
        I = np.array([_i for _i in yI])
        I = I[halfbuf:-halfbuf]
        Q = np.array([_q for _q in yQ])
        Q = Q[halfbuf:-halfbuf]

        ## save record in sigmf format
        save_sigmf(I, Q, metadata, idx_start+i)
                
    return idx_start+i+1

def generate_fsk(idx_start, mod, config):
    verbose = ctypes.c_int(config["verbose"])
    modtype = ctypes.c_int(mod[0])
    n_samps = ctypes.c_int(config["n_samps"]+buf)

    sig_params = [(_sps, _beta, _delay, _dt) for _sps in config["symbol_rate"] for _beta in config["gaussian_filter"]["beta"] for _delay in config["gaussian_filter"]["delay"] for _dt in config["gaussian_filter"]["dt"]]
    idx = np.random.choice(len(sig_params), config["n_captures"])
    sig_params = [sig_params[_idx] for _idx in idx]
    idx = np.random.choice(len(config["channel_params"]), config["n_captures"])
    channel_params = [config["channel_params"][_idx] for _idx in idx]

    for i in range(0, int(config["n_captures"])):
        seed = ctypes.c_int(np.random.randint(1e9))
        snr = ctypes.c_float(channel_params[i][0])
        fo = ctypes.c_float(2.*channel_params[i][1]*np.pi)
        po = ctypes.c_float(0.0) ## assume po = 0.0

        bps = ctypes.c_int(int(np.log2(mod[1])))
        modidx = ctypes.c_float(mod[2])
        sps = ctypes.c_int(sig_params[i][0])
        n_sym = n_sym = ctypes.c_int(int(np.ceil(n_samps.value/sps.value)))
        pulseshape = ctypes.c_int(mod[3])

        beta = ctypes.c_float(sig_params[i][1]) 
        delay = ctypes.c_uint(int(sig_params[i][2]))
        dt = ctypes.c_float(sig_params[i][3])

        ## create return arrays
        s = (ctypes.c_uint * n_sym.value)(*np.zeros(n_sym.value, dtype=int))
        xI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        xQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        yI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        yQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        
        ## calls to c code
        cfsk.fsk_modulate(n_sym, bps, modidx, pulseshape, sps, delay, beta, s, xI, xQ, verbose, seed)
        cchan.channel(snr, n_sym, sps, fo, po, xI, xQ, yI, yQ, verbose, seed)

        if mod[2] == 0.5:
            cs = 2.5e3
        elif mod[2] == 1.0:
            cs = 5e3
        elif mod[2] == 15.0:
            cs = 15e3
        else:
            cs = None
        
        if pulseshape.value == 0:
            ft = "square"
            b = "none"
        else:
            ft = "gaussian"
            b = beta.value

        metadata = {"modname":mod[-1],
                    "modclass":mod[0],
                    "order":mod[1],
                    "mod_idx":modidx.value,
                    "carrier_spacing":cs,
                    "n_samps":n_samps.value-buf,
                    "channel_type":config["channel_type"],
                    "snr":snr.value,
                    "filter_type":ft,
                    "sps":sps.value,
                    "beta":b,
                    "delay":delay.value,
                    "dt":dt.value,
                    "fo":fo.value,
                    "po":po.value,
                    "savepath":config["savepath"],
                    "savename":config["savename"]}

        ## convert to numpy arrays
        I = np.array([_i for _i in yI])
        I = I[halfbuf:-halfbuf]
        Q = np.array([_q for _q in yQ])
        Q = Q[halfbuf:-halfbuf]

        ## save record in sigmf format
        save_sigmf(I, Q, metadata, idx_start+i)

    return idx_start+i+1

def generate_noise(idx_start, mod, config):
    verbose = ctypes.c_int(config["verbose"])
    modtype = ctypes.c_int(mod[0])
    n_samps = ctypes.c_int(config["n_samps"]+buf)

    idx = np.random.choice(len(config["channel_params"]), config["n_captures"])
    channel_params = [config["channel_params"][_idx] for _idx in idx]

    for i in range(0, config["n_captures"]):
        seed = ctypes.c_int(np.random.randint(1e9))
        snr = ctypes.c_float(channel_params[i][0])
        fo = ctypes.c_float(2.*channel_params[i][1]*np.pi)
        po = ctypes.c_float(0.0)
        sps = ctypes.c_int(1)

        xI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        xQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        yI = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))
        yQ = (ctypes.c_float * n_samps.value)(*np.zeros(n_samps.value))

        cchan.channel(snr, n_samps, sps, fo, po, xI, xQ, yI, yQ, verbose, seed)

        metadata = {"modname":mod[-1],
                    "modclass":modtype.value,
                    "n_samps":n_samps.value-buf,
                    "channel_type":config["channel_type"],
                    "snr":snr.value,
                    "sps":sps.value,
                    "fo":fo.value,
                    "po":po.value,
                    "savepath":config["savepath"],
                    "savename":config["savename"]}
        
        ## convert to numpy arrays
        I = np.array([_i for _i in yI])
        I = I[halfbuf:-halfbuf]
        Q = np.array([_q for _q in yQ])
        Q = Q[halfbuf:-halfbuf]

        ## save record in sigmf format
        save_sigmf(I, Q, metadata, idx_start+i)
            
    return idx_start+i+1

def run_tx(config):
    idx = 0

    ## loop through config
    for _mod in config["modulation"]:
        start_idx = idx
        if mod_int2modem[_mod[0]] is None:
            idx = generate_noise(start_idx, _mod, config)
        elif mod_int2modem[_mod[0]] == "linear":
            idx = generate_linear(start_idx, _mod, config)
        elif mod_int2modem[_mod[0]] == "amplitude":
            idx = generate_am(start_idx, _mod, config)
        elif mod_int2modem[_mod[0]] == "frequency":
            idx = generate_fm(start_idx, _mod, config)        
        elif mod_int2modem[_mod[0]] == "freq_shift":
            idx = generate_fsk(start_idx, _mod, config)
        else:
            raise ValueError("Undefined modem.")

        print(_mod[-1] + ": " + str(idx-start_idx))

    if config["archive"]:
        archive_sigmf(config["savepath"])

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", type=str, help="Path to configuration file to use for data generation.")
    args = parser.parse_args()

    with open(args.config_file) as f:
        config = json.load(f)

    with open("./configs/defaults.json") as f:
        defaults = json.load(f)

    config = map_config(config, defaults)

    run_tx(config)
