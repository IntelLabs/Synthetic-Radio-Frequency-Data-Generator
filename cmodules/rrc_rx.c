// 
// rrc_rx.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "rrc_rx.h"
#include "utils.h"

void rrc_rx(int n_sym, int sps, unsigned int delay, float beta, float dt, float yI[], float yQ[], float rs_mI[], float rs_mQ[], int verbose)
{

    // derived values
    unsigned int n_samps = n_sym * sps;
    unsigned int n_sym_pad = n_sym + delay;
    unsigned int n_samps_pad = n_sym_pad * sps;

    // init arrays
    float complex y[n_samps_pad];  // received signal
    for (unsigned int i=0; i<n_samps_pad; i++)
    {
	if (i < n_samps)
	{
	    y[i] = yI[i] + _Complex_I*yQ[i];
	}
	else
	{
	    y[i] = 0. + _Complex_I*0.;
	}
    }
    float complex rs_m[n_sym_pad];	// recieved signal filtered and downsampled

    // create RRC Rx filter
    unsigned int g_len = 2*sps*delay + 1;	// filter length
    float g[g_len];	// filter taps
    liquid_firdes_rrcos(sps, delay, beta, dt, g);
    firdecim_crcf decim = firdecim_crcf_create(sps, g, g_len);
    firdecim_crcf_set_scale(decim, 1.0f/(float)sps);
    if (verbose)
    {
	printf("Rx Filter Taps: \n");
	print_arr_f(g, g_len);
	firdecim_crcf_print(decim);	
    }

    // run rx filter
    for (unsigned int i=0; i<n_sym_pad; i++) {
    	firdecim_crcf_execute(decim, &y[i*sps], &rs_m[i]);
    }
    if (verbose)
    {
	printf("Rx, Filtered and Downsampled:  \n");
	print_arr_complex(rs_m, n_sym_pad);
    }

    // sep IQ
    for (unsigned int i = 0; i<n_sym; i++)
    {
	rs_mI[i] = crealf(rs_m[i+delay]); 	
	rs_mQ[i] = cimagf(rs_m[i+delay]);
    }

    // clean up
    firdecim_crcf_destroy(decim);
}
