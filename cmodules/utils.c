// 
// datagen_utils.c
//

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <complex.h>

#include "utils.h"

void print_arr_complex(complex float arr[], int arrlen)
{
    for (int j = 0; j < arrlen; j++)
	printf("%12.8f + j*%12.8f, ", crealf(arr[j]), cimagf(arr[j]));
    printf("\n \n");
}

void print_arr_int(unsigned int arr[], int arrlen)
{
    for (int j = 0; j < arrlen; j++)
	printf("%d, ", arr[j]);
    printf("\n \n");
}

void print_arr_f(float arr[], int arrlen)
{
    for (int j = 0; j < arrlen; j++)
	printf("%f, ", arr[j]);
    printf("\n \n");
}
