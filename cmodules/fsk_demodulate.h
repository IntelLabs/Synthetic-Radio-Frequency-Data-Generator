// 
// fsk_demodulate.h
//

#ifndef FSK_DEMODULATE_H
#define FSK_DEMODULATE_H

void fsk_demodulate(int n_sym, int bps, float modidx, int pulseshape, int sps, int delay, float beta, float yI[], float yQ[], unsigned int rs[], int verbose);

#endif