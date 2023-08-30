// 
// fsk_modulate.h
//

#ifndef FSK_MODULATE_H
#define FSK_MODULATE_H

void fsk_modulate(int n_sym, int bps, float modidx, int pulseshape, int sps, int delay, float beta, unsigned int s[], float rI[], float rQ[], int verbose, int seed);

#endif