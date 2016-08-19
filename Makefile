# Pushes code to rpi and arduino

all:
	make -C py stop
	make -C py push
	make -C ar push
	make -C ar build
	make -C py restart
