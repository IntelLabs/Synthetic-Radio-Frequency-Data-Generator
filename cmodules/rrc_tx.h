// 
// rrc_tx.h
//

#ifndef RRC_TX_H
#define RRC_TX_H

void rrc_tx(int n_sym, int sps, unsigned int delay, float beta, float dt, float sI[], float sQ[], float xI[], float xQ[], int verbose);

#endif
