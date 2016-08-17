# Pushes code to the raspberry pi and restarts the service to make it use it

TARGET=clayton@clockpi.local
DIR=~/clockpi/py/
VENV=venv

all: push restart

push:
	rsync -r --exclude={$(VENV),Makefile,} * $(TARGET):$(DIR)

requirements:
	ssh $(TARGET) 'cd $(DIR) && source $(VENV)/bin/activate && pip install -r requirements.txt'

try:
	ssh -t $(TARGET) 'cd $(DIR) && source $(VENV)/bin/activate && python clockpi.py'

stop:
	ssh -t $(TARGET) 'sudo service clockpi stop'

start:
	ssh -t $(TARGET) 'sudo service clockpi start'

restart:
	ssh -t $(TARGET) 'sudo service clockpi restart'

benchmark:
	ssh -t $(TARGET) 'cd $(DIR) && source $(VENV)/bin/activate && python run_benchmark.py'

cycle_time:
	ssh -t $(TARGET) 'cd $(DIR) && source $(VENV)/bin/activate && python run_cycle_time_benchmark.py'
