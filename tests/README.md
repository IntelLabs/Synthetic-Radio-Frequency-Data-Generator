The scripts in this directory can be used to confirm that the signal generator is functioning as expected.

 - `txrx_plots.py` shows plots of transmitted symbols, transmitted samples, received samples (Tx samples + AWGN noise), and received symbols, both in the time domain and on the IQ plane
 - `verify_ber.py` plots the bit error rate of the signal generator (without the RRC transmit filter) against theory curves
 - `ber_rrc.py` plots the bit error rate of the signal generator with the RRC transmit filter

Arguments to these scripts must be manually modified within the script.
All scripts are executable and require no command line arguments.

