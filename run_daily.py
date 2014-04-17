#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, datetime, subprocess

os.chdir(os.path.dirname(__file__))

reload(sys)
sys.setdefaultencoding('utf-8')

end_date = datetime.datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime('%Y-%m-%d')

cmd = os.path.join(os.path.abspath('.'), 'ivod_downloader.py')

subprocess.call([cmd, '-s', start_date, '-e', end_date])
