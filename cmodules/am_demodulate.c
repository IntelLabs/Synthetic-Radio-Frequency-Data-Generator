// 
// demodulate.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "am_demodulate.h"
#include "utils.h"

void am_demodulate(int modtype, float mod_idx, int n_samps, float yI[], float yQ[], float rs[], unsigned int delay[], int verbose)
{
    // create demod object 
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
    ampmodem demod   = ampmodem_create(mod_idx, ms, suppressed);
    if (verbose)
    {
    	ampmodem_print(demod);
    }
    delay[0] = (unsigned int) (ampmodem_get_delay_mod(demod) + ampmodem_get_delay_demod(demod));

    // init arrays
    float complex y[n_samps];  // received signal
    for (unsigned int i=0; i<n_samps; i++)
    {
		y[i] = yI[i] + _Complex_I*yQ[i];
    }

    // receiver
    for (int i=0; i<n_samps; i++) 
    {
	    // demod
		ampmodem_demodulate(demod, y[i], &rs[i]);
    }
    if (verbose)
    {
        printf("Received signal: \n");
		print_arr_f(rs, n_samps);
    }

    // clean up
    ampmodem_destroy(demod);
}