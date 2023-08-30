// 
// awgn.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "channel.h"
#include "utils.h"

void channel(float snr, int n_sym, int sps, float fo, float po, float xI[], float xQ[],  float yI[], float yQ[],int verbose, int seed)
{

    if (seed < 0){
    	srand((unsigned) time(0));
    }
    else{
	    srand(seed);
    }

    // derived values
    int n_samps = n_sym*sps;
    float nstd = powf(10.0f, -snr/20.0f);

    // init arrays
    float complex x[n_samps];	// transmitted signal
    for (unsigned int i=0; i<n_samps; i++)
    {
	    x[i] = xI[i] + _Complex_I*xQ[i];
    }

    // fo, awgn, sep IQ
    float complex o = cexpf(_Complex_I*(fo + po));
    float complex x_o;
    float complex n;
    float complex y;
    for (unsigned int i=0; i<n_samps; i++)
    {
        // fo & po
        x_o = (crealf(x[i])*crealf(o)) + (crealf(x[i])*cimagf(o)*_Complex_I) + (cimagf(x[i])*crealf(o)*_Complex_I) + (cimagf(x[i])*cimagf(o)*-1.0);

	    // manual awgn
        n = nstd*(randnf() + _Complex_I*randnf())/sqrtf(2.0f);
        y = x_o + n; 

        // split IQ
	    yI[i] = crealf(y);
	    yQ[i] = cimagf(y);	
    }

}
