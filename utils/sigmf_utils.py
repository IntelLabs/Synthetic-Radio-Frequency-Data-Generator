## python imports
import numpy as np
from datetime import datetime
import sys
import os
import tarfile

## internal imports
# from sigmf import *
import sigmf
from .maps import mod_int2type, mod_int2modem, mod_int2class 
from .maps import mod_int2symbolvariant, am_variants, fm_variants


def archive_sigmf(savepath):
    savepath_ext = savepath + ".sigmf" 
    files = os.listdir(savepath)

    ## NOTE: We assume all .sigmf-data and .sigmf-meta files follow SigMF spec
    with tarfile.open(savepath_ext, mode='w') as out:
        for f in files:
            ## check file extensions
            assert(f[-5:] in ['-data', '-meta']), "Invalid file type found in " + savepath
            out.add(savepath + "/" + f, arcname=f)

def save_sigmf(i, q, config, idx):
    record_name = config["savepath"] + "/" + config["savename"] + "-" + str(idx)
    data_name = record_name + ".sigmf-data"
    meta_name = record_name + ".sigmf-meta"

    ## interleave IQ, save in .sigmf-data file
    iq = np.zeros(2*len(i), dtype=i.dtype)
    iq[0::2] = i
    iq[1::2] = q
    with open(data_name, "wb") as f:
        np.save(f, iq)

    ## create SigMFFile object w/ appropriate metadata
    if sys.byteorder == "little":
        datatype = "cf32_le"
    else:
        datatype = "cf32_be"

    _global = {"core:datatype":"cf32_le", 
               "core:version":"v0.0.1",
               "core:recorder":"liquid-dsp",
               "core:extensions":{"modulation":"v0.0.2",
                                  "channel":"v0.0.1",
                                  "filter":"v0.0.1"}}
    f = sigmf.SigMFFile(data_file=data_name, global_info=_global)
    f.add_capture(0, metadata={"core:length":config["n_samps"], "core:time":datetime.today().isoformat()})
    f.add_annotation(0, config["n_samps"], metadata={"rfml_labels":{"modclass":config["modname"]}})
    if mod_int2modem[config["modclass"]] is None:
        f.add_annotation(0, config["n_samps"], metadata={"channel":{"type":config["channel_type"],
                                                                    "snr":config["snr"],
                                                                    "fo":config["fo"],
                                                                    "po":config["po"]}})
    elif mod_int2modem[config["modclass"]] == "linear":
        f.add_annotation(0, config["n_samps"], metadata={"modulation":{"type":mod_int2type[config["modclass"]],
                                                                        "class":mod_int2class[config["modclass"]],
                                                                        "order":config["order"],
                                                                        "symbol_variant":mod_int2symbolvariant[config["modclass"]]},
                                                         "channel":{"type":config["channel_type"],
                                                                    "snr":config["snr"],
                                                                    "fo":config["fo"],
                                                                    "po":config["po"]},
                                                         "filter":{"type":config["filter_type"],
                                                                    "sps":config["sps"],
                                                                    "delay":config["delay"],
                                                                    "rolloff":config["beta"],
                                                                    "dt":config["dt"]}})
    elif mod_int2modem[config["modclass"]] == "amplitude":
        f.add_annotation(0, config["n_samps"], metadata={"modulation":{"type":mod_int2type[config["modclass"]],
                                                                        "class":mod_int2class[config["modclass"]],
                                                                        "modulation_index":config["mod_idx"],
                                                                        "variant":am_variants[config["modvariant"]]},
                                                         "channel":{"type":config["channel_type"],
                                                                    "snr":config["snr"],
                                                                    "fo":config["fo"],
                                                                    "po":config["po"]}})
    elif mod_int2modem[config["modclass"]] == "frequency":
        f.add_annotation(0, config["n_samps"], metadata={"modulation":{"type":mod_int2type[config["modclass"]],
                                                                        "class":mod_int2class[config["modclass"]],
                                                                        "modulation_factor":config["mod_factor"],
                                                                        "variant":fm_variants[config["modvariant"]]},
                                                         "channel":{"type":config["channel_type"],
                                                                    "snr":config["snr"],
                                                                    "fo":config["fo"],
                                                                    "po":config["po"]}})
    elif mod_int2modem[config["modclass"]] == "freq_shift":
        f.add_annotation(0, config["n_samps"], metadata={"modulation":{"type":mod_int2type[config["modclass"]],
                                                                        "class":mod_int2class[config["modclass"]],
                                                                        "modulation_index":config["mod_idx"],
                                                                        "carrier_spacing":config["carrier_spacing"]},
                                                         "channel":{"type":config["channel_type"],
                                                                    "snr":config["snr"],
                                                                    "fo":config["fo"],
                                                                    "po":config["po"]},
                                                         "filter":{"type":config["filter_type"],
                                                                    "sps":config["sps"],
                                                                    "delay":config["delay"],
                                                                    "beta":config.get("beta", "none"),
                                                                    "dt":config["dt"]} })
    else:
        print("Undefined modem.")
        raise

    with open(meta_name,"w") as mf:
        f.dump(mf, pretty=True)


    return record_name


