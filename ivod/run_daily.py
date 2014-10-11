#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import datetime
import subprocess
import time

os.chdir(os.path.dirname(__file__))

reload(sys)
sys.setdefaultencoding('utf-8')

end_date = datetime.datetime.now().strftime('%Y-%m-%d')
start_date = (
    datetime.datetime.now() -
    datetime.timedelta(
        days=5)).strftime('%Y-%m-%d')

clean_cmd = os.path.join(os.path.abspath('.'), 'cleanup.sh')
run_cmd = os.path.join(os.path.abspath('.'), 'ivod_downloader.py')

subprocess.call([clean_cmd])
time.sleep(5)
subprocess.call([run_cmd, '-s', start_date, '-e', end_date])
time.sleep(5)
subprocess.call([clean_cmd])
