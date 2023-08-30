// 
// fsk_demodulate.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "fsk_demodulate.h"
#include "utils.h"

void fsk_demodulate(int n_sym, int bps, float modidx, int pulseshape, int sps, int delay, float beta, float yI[], float yQ[], unsigned int rs[], int verbose)
{
    // derive values
    unsigned int n_samps = n_sym * sps;
    float complex y[n_samps];

    // filter type
    int filtertype = LIQUID_CPFSK_SQUARE;
    switch(pulseshape){
        case 0: filtertype = LIQUID_CPFSK_SQUARE;   break;
        case 1: filtertype = LIQUID_CPFSK_GMSK;    break;
        printf("Invalid filter type. Defaulting to square.");
    }

    // reconstruct received signal
    for (unsigned int i=0; i<n_samps; i++)
    {
        y[i] = yI[i] + _Complex_I*yQ[i];
    }

    // create modem
    cpfskdem demod = cpfskdem_create(bps, modidx, sps, delay, beta, filtertype);

    // demodulate
    for (unsigned int i=0; i<n_sym; i++)
    {
        rs[i] = cpfskdem_demodulate(demod, &y[i*sps]);
    }

    // clean up
    cpfskdem_destroy(demod);
}
