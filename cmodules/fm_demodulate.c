// 
// fm_demodulate.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "fm_demodulate.h"
#include "utils.h"

void fm_demodulate(float mod_idx, int n_samps, float yI[], float yQ[], float rs[], int verbose)
{
    // create the modem objects
    freqdem demod = freqdem_create(mod_idx);
    if (verbose)
    {
    	freqdem_print(demod);
    }

    // init arrays
    float complex y;  
    for (unsigned int i=0; i<n_samps; i++)
    {
		y = yI[i] + _Complex_I*yQ[i];
        freqdem_demodulate(demod, y, &rs[i]);
    }

    // clean up
    freqdem_destroy(demod);
}