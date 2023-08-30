// 
// fm_modulate.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "fm_modulate.h"
#include "utils.h"

void fm_modulate(float mod_idx, int n_samps, float x[], float rI[], float rQ[], int verbose, int seed)
{

    if (seed < 0){
    	srand((unsigned) time(0));
    }
    else{
		srand(seed);
    }
    
    // create the modem objects
    freqmod mod = freqmod_create(mod_idx);
    if (verbose)
    {
    	freqmod_print(mod);
    }

    // generate fake message signal (sum of sines)
    // NOTE: not ideal, borrowed from liquid-dsp examples
    float r1 = (float)rand()/RAND_MAX;
    r1 = (0.5 - 0.0001) * r1 + 0.0001;
    float r2 = (float)rand()/RAND_MAX;
    r2 = (0.5 - 0.0001) * r2 + 0.0001;
    float r3 = (float)rand()/RAND_MAX;
    r3 = (0.5 - 0.0001) * r3 + 0.0001;
    for (unsigned int i=0; i<n_samps; i++) {
        x[i] = 0.3f*cosf(2*M_PI*r1*i + 0.0f) +
               0.2f*cosf(2*M_PI*r2*i + 0.4f) +
               0.4f*cosf(2*M_PI*r3*i + 1.7f);
    }

    float complex r;
    for (unsigned int i=0; i<n_samps; i++){
        // modulate
        freqmod_modulate(mod, x[i], &r);

        // sep IQ
        rI[i] = crealf(r); 
        rQ[i] = cimagf(r);
    }

    // clean up
    freqmod_destroy(mod);
}
