// 
// rrc_rx.h
//

#ifndef RRC_RX_H
#define RRC_RX_H

void rrc_rx(int n_sym, int sps, unsigned int delay, float beta, float dt, float yI[], float yQ[], float rs_mI[], float rs_mQ[], int verbose);

#endif
