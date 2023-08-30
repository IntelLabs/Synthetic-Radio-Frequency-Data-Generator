
## python imports
import numpy as np
import os
from datetime import datetime

from .maps import mod_str2int

def check_range(x, positive=True):
    start, stop, step = x
    if positive:
        assert [i >= 0.0 for i in x]

    if stop < start:
        return False
    elif step > (stop - start):
        return False
    else:
        return True

def map_config(config, defaults):
    mapped = {}

    ## num samples
    if "n_samps" in config.keys():
        assert isinstance(config["n_samps"], int), "n_samps must be an integer."
        assert config["n_samps"] > 0, "n_samps must be greater than zero."
        mapped["n_samps"] = config["n_samps"]
    else:
        print("No n_samps value provided. Using defaults.")
        mapped["n_samps"] = defaults["n_samps"]

    ## num captures
    if "n_captures" in config.keys():
        assert isinstance(config["n_captures"], int), "n_capures must be an integer."
        assert config["n_captures"] > 0, "n_captures must be greater than zero."
        mapped["n_captures"] = config["n_captures"]
    else:
        print("No n_captures value provided. Using defaults.")
        mapped["n_captures"] = defaults["n_captures"]

    ## mods
    if "modulation" in config.keys():
        try:
            mapped["modulation"] = []
            for i in config["modulation"]:
                mapped["modulation"].append(mod_str2int[i])
        except ValueError:
            print("Invalid modulation scheme found.")
    else:
        print("No modulations value provided. Using defaults.")
        mapped["modulation"] = []
        for i in defaults["modulation"]:
            mapped["modulation"].append(mod_str2int[i])

    ## symbol rate
    if "symbol_rate" in config.keys():
        if isinstance(config["symbol_rate"], list):
            for i in config["symbol_rate"]:
                assert isinstance(i, int), "symbol_rate must be an integer."
                assert i > 0, "symbol_rate must be greater than zero."
            mapped["symbol_rate"] = config["symbol_rate"]
        elif isinstance(config["symbol_rate"], int):
            assert config["symbol_rate"] > 0, "symbol_rate must be greater than zero."
            mapped["symbol_rate"] = [config["symbol_rate"]]
        else:
            raise ValueError("Invalid symbol rate type.")
    else:
        print("No symbol rate provided. Using defaults.")
        mapped["symbol_rate"] = defaults["symbol_rate"]

    ## AM/FM parameters
    mapped["am_defaults"] = {}
    if "am_defaults" in config.keys():
        if "modulation_index" in config["am_defaults"].keys():
            tmp = config["am_defaults"]["modulation_index"]
        else:
            print("No AM modulation index provided. Using defaults.")
            tmp = defaults["am_defaults"]["modulation_index"]
    else:
        print("No AM defaults provided. Using defaults.")
        tmp = defaults["am_defaults"]["modulation_index"]
    if isinstance(tmp, list):
        assert check_range(tmp)
        mapped["am_defaults"]["modulation_index"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
    elif isinstance(tmp, float) and tmp > 0.0:
        mapped["am_defaults"]["modulation_index"] = [tmp]
    else:
        raise ValueError("Invalid AM modulation index.")
    
    mapped["fmnb_defaults"] = {}
    if "fmnb_defaults" in config.keys():
        if "modulation_factor" in config["fmnb_defaults"].keys():
            tmp = config["fmnb_defaults"]["modulation_factor"]
        else:
            print("No FM-NB modulation factor provided. Using defaults.")
            tmp = defaults["fmnb_defaults"]["modulation_factor"]
    else:
        print("No FM-NB defaults provided. Using defaults.")
        tmp = defaults["fmnb_defaults"]["modulation_factor"]
    if isinstance(tmp, list):
        assert check_range(tmp)
        mapped["fmnb_defaults"]["modulation_factor"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
    elif isinstance(tmp, float) and tmp > 0.0:
        mapped["fmnb_defaults"]["modulation_factor"] = [tmp]
    else:
        raise ValueError("Invalid FM-NB modulation factor.")
    
    mapped["fmwb_defaults"] = {}
    if "fmwb_defaults" in config.keys():
        if "modulation_factor" in config["fmwb_defaults"].keys():
            tmp = config["fmwb_defaults"]["modulation_factor"]
        else:
            print("No FM-WB modulation factor provided. Using defaults.")
            tmp = defaults["fmwb_defaults"]["modulation_factor"]
    else:
        print("No FM-WB defaults provided. Using defaults.")
        tmp = defaults["fmwb_defaults"]["modulation_factor"]
    if isinstance(tmp, list):
        assert check_range(tmp)
        mapped["fmwb_defaults"]["modulation_factor"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
    elif isinstance(tmp, float) and tmp > 0.0:
        mapped["fmwb_defaults"]["modulation_factor"] = [tmp]
    else:
        raise ValueError("Invalid FM-WB modulation factor.")
    
    ## filters
    if "filter" in config.keys():
        for i, f in enumerate(config["filter"]):
            if f["type"] in ["rrc", "gaussian"]:
                filter_type = f["type"] + "_filter" 
                mapped[filter_type] = {}

                d = defaults["filter"]
                tmp = [i["type"] == f["type"] for i in d]
                d_i = np.where(tmp)[0][0]

                if "beta" in f.keys():
                    tmp = f["beta"]
                else:
                    print("No filter beta provided. Using defaults.")
                    tmp = d[d_i]["beta"]
                if isinstance(tmp, list):
                    assert check_range(tmp)
                    mapped[filter_type]["beta"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
                elif isinstance(tmp, float) and tmp > 0.0:
                    mapped[filter_type]["beta"] = [tmp]
                else:
                    raise ValueError("Invalid filter beta.")

                if "dt" in f.keys():
                    tmp = f["dt"]
                else:
                    print("No filter dt provided. Using defaults.")
                    tmp = d[d_i]["dt"]
                if isinstance(tmp, list):
                    assert check_range(tmp)
                    mapped[filter_type]["dt"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
                elif isinstance(tmp, float) and tmp >= 0.0:
                    mapped[filter_type]["dt"] = [tmp]
                else:
                    raise ValueError("Invalid filter dt.")

                if "delay" in f.keys():
                    tmp = f["delay"]
                else:
                    print("No filter delay provided. Using defaults")
                    tmp = d[d_i]["delay"]
                if isinstance(tmp, list):
                    assert check_range(tmp)
                    mapped[filter_type]["delay"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
                elif isinstance(tmp, int) and tmp >= 0:
                    mapped[filter_type]["delay"] = [tmp]
                else:
                    raise ValueError("Invalid filter delay.")
            else:
                raise ValueError("Invalid filter type.")
    else:
        print("No filter parameters provided. Using defaults.")
        mapped["rrc_filter"] = {}
        tmp = defaults["filter"][0]["beta"]
        mapped["rrc_filter"]["beta"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
        tmp = defaults["filter"][0]["dt"]
        mapped["rrc_filter"]["dt"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
        tmp = defaults["filter"][0]["delay"]
        mapped["rrc_filter"]["delay"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
        mapped["gaussian_filter"] = {}
        tmp = defaults["filter"][1]["beta"]
        mapped["gaussian_filter"]["beta"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
        tmp = defaults["filter"][1]["dt"]
        mapped["gaussian_filter"]["dt"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
        tmp = defaults["filter"][1]["delay"]
        mapped["gaussian_filter"]["delay"] = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])


    ## channel 
    if "channel" in config.keys():
        if config["channel"]["type"] == "awgn":
            mapped["channel_type"] = "awgn"

            if "snr" in config["channel"].keys():
                tmp = config["channel"]["snr"]
            else:
                print("No channel SNR parameters provided. Using defaults.")
                tmp = defaults["channel"]["snr"]
            if isinstance(tmp, list):
                assert check_range(tmp, positive=False)
                snr_list = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
            elif isinstance(tmp, int):
                snr_list = [tmp]
            else:
                raise ValueError("Invalid SNR range.")
            
            if "fo" in config["channel"].keys():
                tmp = config["channel"]["fo"]
            else:
                tmp = defaults["channel"]["fo"]
            if isinstance(tmp, list):
                assert check_range(tmp, positive=False)
                fo_list = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
            elif isinstance(tmp, float) and tmp >= 0.0:
                fo_list = [tmp]
            else:
                raise ValueError("Invalid FO range.")
            fo_list = [_fo*np.pi for _fo in fo_list]

            if "po" in config["channel"].keys():
                tmp = config["channel"]["po"]
            else:
                tmp = defaults["channel"]["po"]
            if isinstance(tmp, list):
                assert check_range(tmp, positive=False)
                po_list = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
            elif isinstance(tmp, float) and tmp >= 0.0:
                po_list = [tmp]
            else:
                raise ValueError("Invalid FO range.")

            mapped["channel_params"] = [(snr, fo, po) for snr in snr_list for fo in fo_list for po in po_list]

        else:
            raise ValueError("Invalid channel type.")
    else:
        print("No channel parameters provided. Using defaults.")
        mapped["channel_type"] = "awgn"
        tmp = defaults["channel"]["snr"]
        if isinstance(tmp, list):
            assert check_range(tmp, positive=False)
            snr_list = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
        elif isinstance(tmp, int):
            snr_list = [tmp]
        tmp = defaults["channel"]["fo"]
        if isinstance(tmp, list):
            assert check_range(tmp, positive=False)
            fo_list = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
        elif isinstance(tmp, float) and tmp >= 0.0:
            fo_list = [tmp]
        fo_list = [_fo*np.pi for _fo in fo_list]
        tmp = defaults["channel"]["po"]
        if isinstance(tmp, list):
            assert check_range(tmp, positive=False)
            po_list = np.arange(tmp[0], tmp[1]+(0.5*tmp[2]), tmp[2])
        elif isinstance(tmp, float) and tmp >= 0.0:
            po_list = [tmp]

        mapped["channel_params"] = [(snr, fo, po) for snr in snr_list for fo in fo_list for po in po_list]

    ## savename
    if "savepath" in config.keys():
        tmp = config["savepath"]
    else:
        print("No savename provided. Using defaults.")
        tmp = defaults["savepath"]
    if os.path.exists(tmp):
        ## modify pathname with date (DD-MM-YY) and time (H-M-S)
        t = datetime.today()
        mapped["savepath"] = tmp + "_" + t.strftime("%d-%m-%y-%H-%M-%S")
    else:
        mapped["savepath"] = tmp
    os.makedirs(mapped["savepath"])
    mapped["savename"] = mapped["savepath"].split("/")[-1]

    ## verbosity
    if "verbose" in config.keys():
        if config["verbose"] in [0,1]:
            mapped["verbose"] = config["verbose"]
        else:
            raise ValueError("Verbosity may only be 0 or 1")
    else:
        print("No verbosity parameter provided. Using defaults.")
        mapped["verbose"] = defaults["verbose"]

    ## archive
    if "archive" in config.keys():
        assert isinstance(config["archive"], bool), "archive must be a boolean."
        mapped["archive"] = config["archive"]
    else:
        print("No archive parameter provided. Using defaults.")
        mapped["archive"] = defaults["archive"]
    
    return mapped

