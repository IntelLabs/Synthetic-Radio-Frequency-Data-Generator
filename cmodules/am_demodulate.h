// 
// am_demodulate.h
//

#ifndef AM_DEMODULATE_H
#define AM_DEMODULATE_H

void am_demodulate(int modtype, float mod_idx, int n_samps, float yI[], float yQ[], float rs[], unsigned int delay[], int verbose);

#endif