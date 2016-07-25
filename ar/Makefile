# Pushes code to the raspberry pi and tells it to build/send the project to
# the arduino

TARGET=clayton@clockpi.local
DIR=~/clockpi/ar/

all: push build refresh

push:
	rsync -rv --exclude={Makefile,} * $(TARGET):$(DIR)

build:
	ssh -t $(TARGET) 'cd $(DIR) && ino build && sudo ino upload'

refresh:
	ssh -t $(TARGET) 'sudo service clockpi restart'
