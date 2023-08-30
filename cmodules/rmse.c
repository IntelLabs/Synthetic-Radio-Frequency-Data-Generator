// 
// rmse.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <complex.h>
#include <getopt.h>

#include <liquid/liquid.h>
#include "rmse.h"
#include "utils.h"

void rmse(int n_samps, unsigned int delay, float s[], float rs[], float rmse_r[], int verbose)
{
    float se = 0.0;
    for (unsigned int i = delay; i<n_samps; i++)
    {
        se += (s[i-delay] - rs[i]) * (s[i-delay] - rs[i]);
    }
    rmse_r[0] = sqrtf(se / (float) (n_samps-delay));
}