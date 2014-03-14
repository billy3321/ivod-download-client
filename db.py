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
        	comit_code text, filename text, ext text, path text, finished int);'
        #print sql
        self.cursor.execute(sql)

        sql = 'CREATE UNIQUE INDEX IF NOT EXISTS id ON ivod_index (`firm`, `wmvid`);'
        #print sql
        self.cursor.execute(sql)

    def insert_data(self, data):
        #print data
        sql = 'REPLACE INTO ivod_index (`ad`, `session`, `sitting`, `date`, `firm`, `num`, `length`, `wmvid`, \
            `video_url_n`, `video_url_w`, `speaker`, `thumb`, `time`, `summary`, \
            `comit_code`, `filename`, `ext`, `path`, `finished`) VALUES \
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );'
        #print sql

        self.cursor.execute(sql, (data['ad'], data['session'], data['sitting'], data['date'], data['firm'], \
            data['num'], data['length'], data['wmvid'], data['video_url_n'], data['video_url_w'], \
            data['speaker'], data['thumb'], data['time'], data['summary'], data['comit_code'], \
            data['filename'], data['ext'], data['path'], data['finished']))
        self.db.commit()

    def query_if_finished(self, data):
        #print data

        sql = 'SELECT finished FROM ivod_index WHERE `firm` = ? AND `wmvid` = ? ;'
        self.cursor.execute(sql, (data['firm'], data['wmvid']))

        result = self.cursor.fetchall()
        #print result
        if len(result):
            return result[0][0]
        else:
            return 0
