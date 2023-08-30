# Synthetic Radio Frequency Data Generator

Python tool to generate synthetic radio frequency (RF) datasets.

This repo contains code to synthetically generate 22 types of raw RF signals (psk, qam, fsk, analog modulation variants) in an Additive White Gaussian Noise (AWGN) channel via Python wrappers around [liquid-dsp](https://github.com/jgaeddert/liquid-dsp).

## Usage
Datasets are generated using the `generator.py` script.
For example, the following command will generate an example dataset, `./datasets/example.sigmf`.

```
python generator.py ./configs/example.json
``` 

A JSON configuration file must be provided on the command line which contains the desired dataset size, signal types, and signal generation parameters.
Basic error checking is performed in `./utils/config_utils.py`, and defaults parameters (set in `./configs/defaults.json`) are provided for any missing values.
Configuration files should contain the following parameters:

 - `n_captures`: the number of captures to generate per modulation scheme
 - `n_samps`: the number of raw IQ samples per capture
 - `modulations`: the modulation schemes to include in the dataset (may include "bpsk", "qpsk", "8psk", "16psk", "4dpsk", "16qam", "32qam", "64qam", "16apsk", "32apsk", "fsk5k", "fsk75k", "gfsk5k", "gfsk75k", "msk", "gmsk", "fmnb", "fmwb", "dsb", "dsbsc", "lsb", "usb", and "awgn")
 - `symbol_rate`: number of samples per signal, list of desired symbol rates accepted
 - `am_defaults`: default analog modulation parameters, including modulation index in the form [start, stop, step]
 - `fmnb_defaults`: default narrowband frequency modulation parameters, including modulation factor in the form [start, stop, step]
 - `fmwb_defaults`: default wideband frequency modulation parameters, including modulation factor in the form [start, stop, step]
 - `filter`: default transmit filter parameters, including the type of filter (Gaussian or root-raised cosine (RRC)), the excess bandwidth or `beta`, the symbol overlap or `delay`, and the fractional sample delay or `dt` (all gfsk/gmsk signals use Gaussian filters, all remaining fsk/msk signals use square filters, all psk/qam signals use RRC filters)
 - `channel`: synthetic channel parameters, including the type of channel (only AWGN is implemented, currently), signal-to-noise-ratio (`snr`), frequency offset (`fo`), and phase offset (`po`) in the form [start, stop, step]
 - `savepath`: the dataset location
 - `verbose`: 0 for minimal verbosity, 1 for debugging
 - `archive`: create a SigMF archive of dataset when complete

Datasets are saved in SigMF format. 
Each dataset is a *SigMF Archive* composed of multiple *SigMF Recordings*. 
Each *SigMF Recording* contains a single capture, saved as a binary file (.sigmf-data files), with an associated metadata file (.sigmf-meta) containing the parameters used to generate that capture. 
See the [SigMF specification](https://github.com/gnuradio/SigMF/blob/master/sigmf-spec.md) to read more. 

## Requirements & Setup

In addition to the python packages listed in `requirements.txt`, the code in this repo is dependent upon [liquid-dsp](https://github.com/jgaeddert/liquid-dsp). 
To install liquid-dsp, clone the repo linked, and follow the installation instructions in the README. 
Ensure that you rebind your dynamic libraries using `sudo ldconfig`.

Additionally, the first time using the synthetic RF dataset generator, you'll need to run

```
>> cd ./cmodules && make && cd ../
```

>>>>>>> master
