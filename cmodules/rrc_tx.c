// 
// rrc.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "rrc_tx.h"
#include "utils.h"

void rrc_tx(int n_sym, int sps, unsigned int delay, float beta, float dt, float sI[], float sQ[], float xI[], float xQ[], int verbose)
{

    // derived values
    unsigned int n_samps = n_sym * sps;
    unsigned int n_sym_pad = n_sym + delay;
    unsigned int n_samps_pad = n_sym_pad * sps;

    // init arrays
    float complex s_m[n_sym_pad];  // modulated symbols
    for (unsigned int i=0; i<n_sym; i++)
    {
	if (i < n_sym)
	{
	    s_m[i] = sI[i] + _Complex_I*sQ[i];
	}
	else
	{
	    s_m[i] = 0. + _Complex_I*0.;
	}
    }
    if (verbose)
    {
	printf("Tx Symbols: \n");
	print_arr_complex(s_m, n_sym_pad);
    }
    float complex x[n_samps_pad];	// transmitted signal

    // create RRC Tx filter
    unsigned int h_len = 2*sps*delay + 1;	// filter length
    float h[h_len];	// filter taps
    liquid_firdes_rrcos(sps, delay, beta, dt, h);
    firinterp_crcf interp = firinterp_crcf_create(sps, h, h_len);
    if (verbose)
    {
	printf("Tx Filter Taps: \n");
	print_arr_f(h, h_len);
	firinterp_crcf_print(interp);	
    }

    // run transmit filter
    for (unsigned int i=0; i<n_sym_pad; i++) {
	firinterp_crcf_execute(interp, s_m[i], &x[i*sps]);
    }
    if (verbose)
    {
	printf("Tx Samples:  \n");
	print_arr_complex(x, n_samps_pad);
    }

    // sep IQ
    unsigned int pad = delay * sps;
    for (unsigned int i = 0; i<n_samps; i++)
    {
	xI[i] = crealf(x[i + pad]); 	
	xQ[i] = cimagf(x[i + pad]);
    }

    // clean up
    firinterp_crcf_destroy(interp);
}
