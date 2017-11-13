# Pushes code to the raspberry pi and restarts the service to make it use it

TARGET=clayton@clockpi.local
DIR=~/clockpi/py/clockpi/
VENV=venv

all: push restart

push:
	rsync -r --exclude={$(VENV),Makefile,} * $(TARGET):$(DIR)
	ssh $(TARGET) 'cd $(DIR) && find clockpi -name *.pyc -delete'

requirements: push
	ssh $(TARGET) 'cd $(DIR) && source $(VENV)/bin/activate && pip install -r requirements.txt'

stop:
	./shmake.sh $(TARGET) stop

start:
	./shmake.sh $(TARGET) start

restart:
	./shmake.sh $(TARGET) restart

log:
	ssh $(TARGET) -t 'sudo tail -F -n 50 /var/log/clockpi.log'

benchmark: stop push
	ssh -t $(TARGET) 'cd $(DIR) && source $(VENV)/bin/activate && python run_benchmark.py'

cycle_time: stop push
	ssh -t $(TARGET) 'cd $(DIR) && export PYTHONPATH=$$PYTHONPATH:$$PWD/clockpi && source $(VENV)/bin/activate && python run_cycle_time_benchmark.py'

font_test: stop push
	ssh -t $(TARGET) 'cd $(DIR) && export PYTHONPATH=$$PYTHONPATH:$$PWD/clockpi && source $(VENV)/bin/activate && python clockpi/run_font_test.py'

sun_test: stop push
	ssh -t $(TARGET) 'cd $(DIR) && export PYTHONPATH=$$PYTHONPATH:$$PWD/clockpi && source $(VENV)/bin/activate && python clockpi/run_sun_test.py'
