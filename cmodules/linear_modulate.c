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
#include "linear_modulate.h"
#include "utils.h"

void linear_modulate(int modtype, int order, int n_sym, unsigned int s[], float rI[], float rQ[], int verbose, int seed)
{

    if (seed < 0){
    	srand((unsigned) time(0));
    }
    else{
		srand(seed);
    }

    // create mod/demod objects
    modulation_scheme ms = LIQUID_MODEM_QAM16;
    switch(modtype){
		case 1:
			switch(order){
				// PSK
				case 2:		ms = LIQUID_MODEM_BPSK;		break;
				case 4:		ms = LIQUID_MODEM_QPSK;		break;
				case 8:		ms = LIQUID_MODEM_PSK8;		break;
				case 16:	ms = LIQUID_MODEM_PSK16;	break;
				case 32:	ms = LIQUID_MODEM_PSK32;	break;
				case 64:	ms = LIQUID_MODEM_PSK64;	break;
				case 128:	ms = LIQUID_MODEM_PSK128;	break;
				case 256:	ms = LIQUID_MODEM_PSK256;	break;
				printf("Invalid modulation order. Defaulting to 16QAM.\n"); 
			}
			break;
		case 2:
			switch(order){
				// QAM
				case 4:		ms = LIQUID_MODEM_QAM4;		break;
				case 8:		ms = LIQUID_MODEM_QAM8;		break;
				case 16:	ms = LIQUID_MODEM_QAM16;	break;
				case 32:	ms = LIQUID_MODEM_QAM32;	break;
				case 64:	ms = LIQUID_MODEM_QAM64;	break;
				case 128:	ms = LIQUID_MODEM_QAM128;	break;
				case 256:	ms = LIQUID_MODEM_QAM256;	break;
				printf("Invalid modulation order. Defaulting to 16QAM.\n"); 
			}
			break;
		case 3:
			switch(order){
				// ASK
				case 2:		ms = LIQUID_MODEM_ASK2;		break;
				case 4:		ms = LIQUID_MODEM_ASK4;		break;
				case 8:		ms = LIQUID_MODEM_ASK8;		break;
				case 16:	ms = LIQUID_MODEM_ASK16;	break;
				case 32:	ms = LIQUID_MODEM_ASK32;	break;
				case 64:	ms = LIQUID_MODEM_ASK64;	break;
				case 128:	ms = LIQUID_MODEM_ASK128;	break;
				case 256:	ms = LIQUID_MODEM_ASK256;	break;
				printf("Invalid modulation order. Defaulting to 16QAM.\n"); 
			}
			break;
		case 4:
			switch(order){
				// APSK
				case 4:		ms = LIQUID_MODEM_APSK4;	break;
				case 8:		ms = LIQUID_MODEM_APSK8;	break;
				case 16:	ms = LIQUID_MODEM_APSK16;	break;
				case 32:	ms = LIQUID_MODEM_APSK32;	break;
				case 64:	ms = LIQUID_MODEM_APSK64;	break;
				case 128:	ms = LIQUID_MODEM_APSK128;	break;
				case 256:	ms = LIQUID_MODEM_APSK256;	break;
				printf("Invalid modulation order. Defaulting to 16QAM.\n"); 
			}
			break;
		case 5:
			switch(order){
				// DPSK
				case 2:		ms = LIQUID_MODEM_DPSK2;	break;
				case 4:		ms = LIQUID_MODEM_DPSK4;	break;
				case 8:		ms = LIQUID_MODEM_DPSK8;	break;
				case 16:	ms = LIQUID_MODEM_DPSK16;	break;
				case 32:	ms = LIQUID_MODEM_DPSK32;	break;
				case 64:	ms = LIQUID_MODEM_DPSK64;	break;
				case 128:	ms = LIQUID_MODEM_DPSK128;	break;
				case 256:	ms = LIQUID_MODEM_DPSK256;	break;
				printf("Invalid modulation order. Defaulting to 16QAM.\n"); 
			}
			break;
		printf("Invalid modulation type. Defaulting to 16QAM.\n");
    }

    // create the modem objects
    modem mod   = modem_create(ms);
    if (verbose)
    {
    	modem_print(mod);
    }

    // generate symbols
    float complex s_m; // modulated symbol
    for (unsigned int i=0; i<n_sym; i++) 
    {
	// generate random input symbol
	s[i] = modem_gen_rand_sym(mod);

	// modulate
	modem_modulate(mod, s[i], &s_m);

	// sep IQ
	rI[i] = crealf(s_m); 
	rQ[i] = cimagf(s_m);
    }

    // clean up
    modem_destroy(mod);
}
