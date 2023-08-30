// 
// ber.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "ber.h"
#include "utils.h"

void ber(int n_sym, int bps, unsigned int s[], unsigned int rs[], float ber_r[], int verbose)
{
    // count bit errors
    unsigned int bit_err = 0;
    for (int i=0; i<n_sym; i++) 
    {
	bit_err += count_bit_errors(s[i], rs[i]);
    }

    // calculate ber
    unsigned int total_bits =  n_sym * bps;
    ber_r[0] = (float) bit_err / total_bits;

    if (verbose)
    {
    	printf("Bit Errors:  %d\n", bit_err);
    	printf("Total Bits:  %d\n", total_bits);
    	printf("BER:  %f\n", ber_r[0]);
    }
}
