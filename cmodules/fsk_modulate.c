// 
// fsk_modulate.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "fsk_modulate.h"
#include "utils.h"

void fsk_modulate(int n_sym, int bps, float modidx, int pulseshape, int sps, int delay, float beta, unsigned int s[], float rI[], float rQ[], int verbose, int seed)
{
    if (seed < 0){
    	srand((unsigned) time(0));
    }
    else{
		srand(seed);
    }

    // derive values
    unsigned int  M = 1 << bps;
    unsigned int n_samps = n_sym * sps;
    float complex x[n_samps];

    // filter type
    int filtertype = LIQUID_CPFSK_SQUARE;
    switch(pulseshape){
        case 0: filtertype = LIQUID_CPFSK_SQUARE;   break;
        case 1: filtertype = LIQUID_CPFSK_GMSK;    break;
        printf("Invalid filter type. Defaulting to square.");
    }

    // create modem
    cpfskmod mod = cpfskmod_create(bps, modidx, sps, delay, beta, filtertype);

    // generate symbols
    for (unsigned int i=0; i<n_sym; i++)
    {
        s[i] = rand() % M;
    }

    // modulate
    for (unsigned int i=0; i<n_sym; i++)
    {
        cpfskmod_modulate(mod, s[i], &x[sps*i]);
    }

    // split IQ
    for (unsigned int i=0; i<n_samps; i++)
    {
        rI[i] = crealf(x[i]); 
	    rQ[i] = cimagf(x[i]);
    }

    // clean up
    cpfskmod_destroy(mod);
}