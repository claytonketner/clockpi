# Pushes code to the raspberry pi and tells it to build/send the project to
# the arduino

TARGET=clayton@clockpi.local
DIR=~/clockpi/ar/
BOARD=uno  # Use `ino list-models` for a list

all: push stop build restart

push:
	rsync -r --exclude={Makefile,} * $(TARGET):$(DIR)

build:
	ssh -t $(TARGET) 'cd $(DIR) && ino build && ino upload -m $(BOARD)'

restart:
	make -C ../py restart

stop:
	make -C ../py stop
