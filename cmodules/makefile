
.PHONY: all clean

all: fsk_modulate fsk_demodulate am_modulate am_demodulate fm_modulate fm_demodulate linear_modulate linear_demodulate rrc_tx rrc_rx channel ber rmse

am_modulate: am_modulate.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC  utils.c am_modulate.o -o am_modulate -lm -lc  -lliquid
	
am_modulate.o: am_modulate.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o am_modulate.o am_modulate.c

am_demodulate: am_demodulate.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC  utils.c am_demodulate.o -o am_demodulate -lm -lc  -lliquid
	
am_demodulate.o: am_demodulate.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o am_demodulate.o am_demodulate.c


fsk_modulate: fsk_modulate.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC  utils.c fsk_modulate.o -o fsk_modulate -lm -lc  -lliquid
	
fsk_modulate.o: fsk_modulate.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o fsk_modulate.o fsk_modulate.c

fsk_demodulate: fsk_demodulate.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC  utils.c fsk_demodulate.o -o fsk_demodulate -lm -lc  -lliquid
	
fsk_demodulate.o: fsk_demodulate.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o fsk_demodulate.o fsk_demodulate.c


fm_modulate: fm_modulate.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC  utils.c fm_modulate.o -o fm_modulate -lm -lc  -lliquid
	
fm_modulate.o: fm_modulate.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o fm_modulate.o fm_modulate.c

fm_demodulate: fm_demodulate.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC  utils.c fm_demodulate.o -o fm_demodulate -lm -lc  -lliquid
	
fm_demodulate.o: fm_demodulate.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o fm_demodulate.o fm_demodulate.c


linear_modulate: linear_modulate.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC  utils.c linear_modulate.o -o linear_modulate -lm -lc  -lliquid
	
linear_modulate.o: linear_modulate.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o linear_modulate.o linear_modulate.c	

linear_demodulate: linear_demodulate.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC  utils.c linear_demodulate.o -o linear_demodulate -lm -lc  -lliquid
	
linear_demodulate.o: linear_demodulate.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o linear_demodulate.o linear_demodulate.c	


rrc_tx: rrc_tx.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC utils.c rrc_tx.o -o rrc_tx -lm -lc -lliquid 

rrc_tx.o: rrc_tx.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o rrc_tx.o rrc_tx.c

rrc_rx: rrc_rx.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC utils.c rrc_rx.o -o rrc_rx -lm -lc -lliquid 

rrc_rx.o: rrc_rx.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o rrc_rx.o rrc_rx.c


channel: channel.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC utils.c channel.o -o channel -lm -lc -lliquid 

channel.o: channel.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o channel.o channel.c


ber: ber.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC ber.o -o ber -lm -lc -lliquid 

ber.o: ber.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o ber.o ber.c


rmse: rmse.o
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC rmse.o -o rmse -lm -lc -lliquid 

rmse.o: rmse.c
	gcc -g -O2  -msse4.1 -shared  -Wall -fPIC -I.  -c -o rmse.o rmse.c


clean:
	rm -rf *.o
	rm -rf ber rmse fsk_modulate fsk_demodulate am_modulate am_demodulate fm_modulate fm_demodulate linear_modulate linear_demodulate rrc_tx rrc_rx channel


