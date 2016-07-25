# Pushes code to the raspberry pi and restarts the service to make it use it

TARGET=clayton@clockpi.local
DIR=~/clockpi/py/
VENV=venv

all: push requirements refresh

push:
	rsync -rv --exclude={$(VENV),Makefile,} * $(TARGET):$(DIR)

requirements:
	ssh $(TARGET) 'cd $(DIR) && source $(VENV)/bin/activate && pip install -r requirements.txt'

refresh:
	ssh -t $(TARGET) 'sudo service clockpi restart'
