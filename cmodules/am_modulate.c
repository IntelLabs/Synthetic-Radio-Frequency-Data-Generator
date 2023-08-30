// 
// linear_modulate.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "am_modulate.h"
#include "utils.h"

void am_modulate(int modtype, float mod_idx, int n_samps, float x[], float rI[], float rQ[], int verbose, int seed)
{

    if (seed < 0){
    	srand((unsigned) time(0));
    }
    else{
		  srand(seed);
    }

    // create mod objects
    modulation_scheme ms = LIQUID_AMPMODEM_DSB;
    int suppressed = 0;
    switch(modtype){
		case 0:
			ms = LIQUID_AMPMODEM_DSB;
			break;
		case 1:
			ms = LIQUID_AMPMODEM_DSB;
            suppressed = 1;
			break;
		case 2:
			ms = LIQUID_AMPMODEM_USB;
			break;
		case 3:
            ms = LIQUID_AMPMODEM_LSB;
            break;
		printf("Invalid modulation type. Defaulting to DSB.\n");
    }

    // create the modem objects
    ampmodem mod   = ampmodem_create(mod_idx, ms, suppressed);
    if (verbose)
    {
    	ampmodem_print(mod);
    }

    // generate fake audio signal (simple windowed sum of tones)
    // NOTE: not ideal, borrowed from liquid-dsp examples
    unsigned int nw = (unsigned int)(0.90*n_samps); // window length
    unsigned int nt = (unsigned int)(0.05*n_samps); // taper length
    float r1 = (float)rand()/RAND_MAX;
    r1 = (0.05 - 0.0001) * r1 + 0.0001;
    float r2 = (float)rand()/RAND_MAX;
    r2 = (0.05 - 0.0001) * r2 + 0.0001;
    for (unsigned int i=0; i<n_samps; i++) 
    {        
        x[i] =  0.6f*cos(2*M_PI*r1*i);
        x[i] += 0.4f*cos(2*M_PI*r2*i);
        x[i] *= i < nw ? liquid_rcostaper_window(i,nw,nt) : 0;
    }

    float complex x_m;
    for (unsigned int i=0; i<n_samps; i++){
        // modulate
        ampmodem_modulate(mod, x[i], &x_m);

        // sep IQ
        rI[i] = crealf(x_m); 
        rQ[i] = cimagf(x_m);
    }

    // clean up
    ampmodem_destroy(mod);
}
