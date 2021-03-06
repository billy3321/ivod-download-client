# -*- coding: utf-8 -*-
from .request import get_json_content
from .request import PresetURL
from .ivod_parser import extract_manifest_from_player_page
from .downloader import download_adobe_hds
from .downloader import download_adobe_hds
from .ivod_parser import extract_manifest_from_player_page

from . import db


import os
import urllib
import urllib2
import json
import cookielib
import sys
import random
import time
import datetime
import subprocess

from optparse import OptionParser

committee = {
    '19': {'name': u'院會', 'code': 'YS'},
    '1': {'name': u'內政', 'code': 'IAD'},
    '17': {'name': u'外交及國防', 'code': 'FND'},
    '5': {'name': u'經濟', 'code': 'ECO'},
    '6': {'name': u'財政', 'code': 'FIN'},
    '8': {'name': u'教育及文化', 'code': 'EDU'},
    '9': {'name': u'交通', 'code': 'TRA'},
    '18': {'name': u'司法及法制', 'code': 'JUD'},
    '12': {'name': u'社會福利及衛生環境', 'code': 'SWE'},
    '13': {'name': u'程序', 'code': 'PRO'},
    '23': {'name': u'紀律', 'code': 'DIS'}}


def download_single_high_quality_video(url):
    play_info = extract_manifest_from_player_page(
        url,
        ensure_high_quality_video=True)

    if play_info:
        return download_adobe_hds(play_info['manifest'], play_info['filename'])
    else:
        sys.stderr.write('get_movie_url content error')
        return False


def list_meeting_date_of_committee(comt, start_date=None, end_date=None):

    try:
        if not start_date:
            start_date = '2011-01-01'
        if not end_date:
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')

        json = get_json_content(PresetURL.COMMS_DATE, {'comtid': comt})
        if json:
            date_list = []
            for i in json['mdate']:
                if end_date >= i['METDAT'] >= start_date:
                    date_list.append(i['METDAT'])
            return date_list
        else:
            sys.stderr.write(
                'get_date_list content error, comtid: %s\n' %
                comt)
            return False
    except:
        sys.stderr.write('get_date_list web error, comtid: %s\n' % comt)
        return False


def list_meeting_video_of_committee(comit, date, page=1):
    json = get_json_content(
        PresetURL.MOVIE_BY_DATE, {
            'comtid': comit, 'date': date, 'page': page})
    if json:
        return json
    else:
        sys.stderr.write(
            'get_movie_by_date content error, comit: %s, date: %s\n' %
            (comit, date))
        return False


def generate_video_url(wzs_id, t, quality='w'):

    if t == 'whole':
        url_part = 'Full'
    elif t == 'clip':
        url_part = 'VOD'
    else:
        return False
    if quality == 'w':
        url = 'https://ivod.ly.gov.tw/Play/%s/%s/1M' % (url_part, wzs_id)
    elif quality == 'n':
        url = 'https://ivod.ly.gov.tw/Play/%s/%s/300K' % (url_part, wzs_id)
    else:
        return False

    script_text = extract_manifest_from_player_page(url)['manifest']
    if script_text:
        return script_text
    else:
        sys.stderr.write(
            'get_movie_url content error, wzs_id: %s, t: %s\n' %
            (wzs_id, t))
        return False


def check_url(url):
    req = None
    try:
        req = urllib.urlopen(url)
        return req.getcode() == 200
    except:
        return False


def check_file_downloaded(path, filename):
    return os.path.exists(os.path.join(path, filename))


def json_dumps(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False).encode('utf8')


def write_config(info, path):
    # print info
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = os.path.join(path, 'info.json')
    if os.path.exists(full_path):
        os.remove(full_path)
    with open(full_path, 'w') as f:
        f.write(json_dumps(info) + '\n')


def get_picture_url(pic_name):
    return 'https://ivod.ly.gov.tw/Image/Pic/' + pic_name


def download_job(item, limit_speed=0):
    path = item['path']
    filename = item['filename']
    return_code1 = 0
    return_code2 = 0
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.path.isdir(path):
        os.remove(path)
        os.makedirs(path)

    if 'thumb' in item and item['thumb'] and check_url(item['thumb']):
        extension = os.path.splitext(item['thumb'])[-1]
        full_path = '%s/%s%s' % (path, filename, extension)
        if os.path.exists(full_path):
            os.remove(full_path)
        urllib.urlretrieve(item['thumb'], full_path)

    if 'video_url_n' in item and item[
            'video_url_n'] and check_url(item['video_url_n']):
        filename_n = '%s_n.flv' % filename

        if item['firm'] == 'whole':
            print u'開始嘗試下載%s的%s委員會窄頻完整影片' % (item['date'], committee[item['comit_code']]['name'])
        elif item['firm'] == 'clip':
            print u'開始嘗試下載%s的%s委員會，第%s段%s窄頻發言片段' % (item['date'], committee[item['comit_code']]['name'], item['num'], item['speaker'])
        print u'影片網址為：%s' % item['video_url_n']

        return_code1 = download_adobe_hds(
            item['video_url_n'],
            filename_n,
            outdir=path,
            maxspeed=str(limit_speed))

        if not os.path.exists(os.path.join(path, filename_n)):
            sys.stderr.write(
                'download_resource error, path: %s, video_url_n: %s\n' %
                (item['video_url_n'], item['filename']))
            sys.stderr.write(
                u'下載%s的%s委員會，第%s段%s窄頻發言片段失敗\n' %
                (item['date'],
                 committee[
                    item['comit_code']]['name'],
                    item['num'],
                    item['speaker']))
            return_code1 = 1

    if 'video_url_w' in item and item[
            'video_url_w'] and check_url(item['video_url_w']):
        filename_w = '%s_w.flv' % filename

        if item['firm'] == 'whole':
            print u'開始嘗試下載%s的%s委員會寬頻完整影片' % (item['date'], committee[item['comit_code']]['name'])
        elif item['firm'] == 'clip':
            print u'開始嘗試下載%s的%s委員會，第%s段%s寬頻發言片段' % (item['date'], committee[item['comit_code']]['name'], item['num'], item['speaker'])
        print u'影片網址為：%s' % item['video_url_n']
        return_code2 = download_adobe_hds(
            item['video_url_w'],
            filename_w,
            outdir=path,
            maxspeed=str(limit_speed))
        if not os.path.exists(os.path.join(path, filename_w)):
            sys.stderr.write(
                'download_resource error, path: %s, video_url_w: %s\n' %
                (item['video_url_w'], item['filename']))
            sys.stderr.write(
                u'下載%s的%s委員會，第%s段%s寬頻發言片段失敗\n' %
                (item['date'],
                 committee[
                    item['comit_code']]['name'],
                    item['num'],
                    item['speaker']))
            return_code2 = 1

    if return_code1 == 0 and return_code2 == 0:
        return 1
    else:
        return 0


def random_sleep():
    time.sleep(random.randint(1, 5))


def load_configurations(path):
    """parser the config"""
    try:
        with open(path) as json_data:
            data = json.load(json_data)
        return data
    except:
        config = {
            "db": {
                "path": "ivod.db"
            },
            "download": {
                "path": "data"
            }
        }
        return config


def download_meetings(
        config, comit_code, start_date, end_date, limit_speed=0, metadata_only=False):

    database = db.Database(config['db'])

    for comit_id in committee.keys():
        if not comit_code or comit_code == committee[comit_id]['code']:
            print u'開始掃描%s委員會可以抓取的影片...' % committee[comit_id]['name']
            date_list = list_meeting_date_of_committee(
                comit_id,
                start_date,
                end_date)
            if not date_list:
                date_list = []
            date_list.sort(reverse=True)
            print date_list
            for date in date_list:
                random_sleep()
                movie_list = list_meeting_video_of_committee(comit_id, date, 1)
                page_num = (int(movie_list['total']) / 5) + 1
                full_list = []
                single_list = []
                for i in movie_list['full']:
                    # print i
                    item = {}
                    item['firm'] = 'whole'
                    item['wmvid'] = i['MEREID']
                    item['ad'] = i['STAGE_']
                    item['session'] = i['DUTION']
                    item['sitting'] = None
                    item['time'] = i['ST_TIM'].split(' ')[1]
                    item['video_url_n'] = generate_video_url(
                        i['MEREID'],
                        'whole',
                        'n')
                    item['video_url_w'] = generate_video_url(
                        i['MEREID'],
                        'whole',
                        'w')
                    item['date'] = i['ST_TIM'].split(' ')[0]
                    item['summary'] = i['METDEC'].replace('\n', '')
                    item['comit_code'] = comit_id
                    item[
                        'filename'] = '%s-%s' % (item['date'], committee[item['comit_code']]['code'])
                    item['path'] = os.path.join(
                        config['download']['path'],
                        item['ad'],
                        item['session'],
                        committee[
                            item['comit_code']]['code'],
                        item['date'])
                    item['num'] = None
                    item['ext'] = 'flv'
                    item['length'] = None
                    item['speaker'] = None
                    item['thumb'] = None
                    if check_file_downloaded(item['path'], (item[
                                             'filename'] + '_n.flv')) and check_file_downloaded(item['path'], (item['filename'] + '_w.flv')):
                        item['finished'] = 1
                    else:
                        item['finished'] = 0
                    #item['finished'] = database.query_if_finished(item)
                    full_list.append(item)
                    random_sleep()
                    # print item
                    if not metadata_only and not item['finished']:
                        item['finished'] = download_job(item, limit_speed)
                        random_sleep()
                        # retry once
                        if not item['finished']:
                            item['finished'] = download_job(item, limit_speed)
                            random_sleep()
                    database.insert_data(item)
                for num in xrange(1, (page_num + 1)):
                    if num != 1:
                        movie_list = list_meeting_video_of_committee(
                            comit_id,
                            date,
                            num)
                    for i in movie_list['result']:
                        item = {}
                        # print i
                        item['wmvid'] = i['WZS_ID']
                        item['firm'] = 'clip'
                        item['ad'] = i['STAGE_']
                        item['session'] = i['DUTION']
                        item['sitting'] = None
                        item['length'] = i['MOVTIM']
                        item['video_url_n'] = generate_video_url(
                            i['WZS_ID'],
                            'clip',
                            'n')
                        item['video_url_w'] = generate_video_url(
                            i['WZS_ID'],
                            'clip',
                            'w')
                        item['speaker'] = i['CH_NAM']
                        item['thumb'] = get_picture_url(i['PHOTO_'])
                        item['time'] = i['ST_TIM'].split(' ')[1]
                        item['date'] = i['ST_TIM'].split(' ')[0]
                        item['summary'] = i['METDEC'].replace('\n', '')
                        item['num'] = i['R']
                        item['comit_code'] = comit_id
                        item['ext'] = 'flv'
                        item['filename'] = '%s-%s-%s-%s' % (item['date'],
                                                            committee[
                            item['comit_code']]['code'],
                            item['num'],
                            item['speaker'])
                        item['path'] = os.path.join(
                            config['download']['path'],
                            item['ad'],
                            item['session'],
                            committee[
                                item['comit_code']]['code'],
                            item['date'])
                        #item['finished'] = database.query_if_finished(item)
                        if check_file_downloaded(item['path'], (item[
                                                 'filename'] + '_n.flv')) and check_file_downloaded(item['path'], (item['filename'] + '_w.flv')):
                            item['finished'] = 1
                        else:
                            item['finished'] = 0
                        single_list.append(item)
                        random_sleep()
                        # print item
                        if not metadata_only and not item['finished']:
                            item['finished'] = download_job(item, limit_speed)
                            random_sleep()
                            # retry once
                            if not item['finished']:
                                item['finished'] = download_job(
                                    item,
                                    limit_speed)
                                random_sleep()
                        database.insert_data(item)
                # print full_list
                # print single_list
                full_info = {'whole': full_list, 'clips': single_list}
                write_config(full_info, config['download']['path'])
