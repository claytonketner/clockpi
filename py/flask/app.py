from constants import TIMER_DATE_TIME_FORMAT
from constants import TIMER_FILE
from datetime import datetime
from datetime import timedelta
from flask import Flask
app = Flask(__name__)


@app.route('/timer/<int:minutes>/<int:seconds>')
def start_timer(minutes, seconds):
    timer_end = datetime.now() + timedelta(minutes=minutes, seconds=seconds)
    timer_end_str = datetime.strftime(timer_end, TIMER_DATE_TIME_FORMAT)
    timer_file = open(TIMER_FILE, 'w')
    timer_file.write(timer_end_str)
    timer_file.close()
    return '{mins} minute, {sec} seconds timer started'.format(
        mins=minutes, sec=seconds)
