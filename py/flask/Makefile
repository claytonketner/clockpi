# Pushes code to the raspberry pi and restarts the service to make it use it

TARGET=clayton@clockpi.local
DIR=~/clockpi/py/flask/
VENV=venv

all: push restart

push:
	rsync -r --exclude={$(VENV),Makefile,} * $(TARGET):$(DIR)
	ssh $(TARGET) 'cd $(DIR) && find . -name "*.pyc" -delete'

requirements:
	ssh $(TARGET) 'cd $(DIR) && source $(VENV)/bin/activate && pip install -r requirements.txt'

stop:
	ssh -t $(TARGET) 'sudo service clockpi_server stop'

start:
	ssh -t $(TARGET) 'sudo service clockpi_server start'

restart:
	ssh -t $(TARGET) 'sudo service clockpi_server restart'
