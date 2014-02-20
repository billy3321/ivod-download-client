#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

class Database(Singleton):
    def __init__(self, config):
        self.config = config
        self.db = None
        self.cursor = None
        self.connect()

    def connect(self):
        if not self.db:
            self.db = sqlite3.connect(self.config['path'])
            self.cursor = self.db.cursor()
            self.create_table()
    def create_table(self):
        sql = 'create table if not exists ivod_index (ad text, \
        	session text, sitting text, date text, firm text, num text, \
            length text, wmvid text, video_url_n text, video_url_w text, \
            speaker text, thumb text, time text, summary text,\
        	comit_code text, filename text, ext text, path text, finished int)'
        self.cursor.execute(sql)
        sql = 'CREATE UNIQUE INDEX id ON ivod_index (ad, session, sitting, date, firm, no);'
        self.cursor.execute(sql)

    def insert_data(self, data):
        sql = '(ad, session, sitting, date, firm, num, length, wmvid, \
            video_url_n, video_url_w, speaker, thumb, time, summary, \
            comit_code, filename, ext, path, finished) VALUES (%(ad)s, \
            %(session)s, %(sitting)s, %(date)s, %(firm)s, %(num)s, \
            %(length)s, %(wmvid)s, %(video_url_n)s, %(video_url_w)s, \
            %(speaker)s, %(thumb)s, %(time)s, %(summary)s, %(comit_code)s, \
            %(filename)s, %(ext)s, %(path)s, %(finished)d )' % data
        self.cursor.execute(sql)