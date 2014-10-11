# -*- coding: utf-8 -*-
from request import get_json_content
from request import PresetURL
from ivod_parser import extract_manifest_from_player_page
from downloader import download_adobe_hds
from downloader import download_adobe_hds
from ivod_parser import extract_manifest_from_player_page


import os, urllib, urllib2, json, cookielib, sys, random, time, datetime, subprocess

from optparse import OptionParser

committee ={
    '19':{'name': u'院會', 'code': 'YS'},
    '1':{'name': u'內政', 'code': 'IAD'},
    '17':{'name': u'外交及國防', 'code': 'FND'},
    '5':{'name': u'經濟', 'code': 'ECO'},
    '6':{'name': u'財政', 'code': 'FIN'},
    '8':{'name': u'教育及文化', 'code': 'EDU'},
    '9':{'name': u'交通', 'code': 'TRA'},
    '18':{'name': u'司法及法制', 'code': 'JUD'},
    '12':{'name': u'社會福利及衛生環境', 'code': 'SWE'},
    '13':{'name': u'程序', 'code': 'PRO'},
    '23':{'name': u'紀律', 'code': 'DIS'}}



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
            sys.stderr.write('get_date_list content error, comtid: %s\n' % comt)
            return False
    except:
        sys.stderr.write('get_date_list web error, comtid: %s\n' % comt)
        return False

def list_meeting_video_of_committee(comit, date, page=1):
    json = get_json_content(PresetURL.MOVIE_BY_DATE, {'comtid': comit, 'date': date, 'page': page})
    if json:
        return json
    else:
        sys.stderr.write('get_movie_by_date content error, comit: %s, date: %s\n' % (comit, date))
        return False

def generate_video_url(wzs_id, t, quality='w'):

    if t == 'whole':
        url_part = 'Full'
    elif t == 'clip':
        url_part = 'VOD'
    else:
        return False
    if quality == 'w':
        url = 'http://ivod.ly.gov.tw/Play/%s/%s/1M' % (url_part, wzs_id)
    elif quality == 'n':
        url = 'http://ivod.ly.gov.tw/Play/%s/%s/300K' % (url_part, wzs_id)
    else:
        return False
    
    script_text = extract_manifest_from_player_page(url)['manifest']
    if script_text:
        return script_text
    else:
        sys.stderr.write('get_movie_url content error, wzs_id: %s, t: %s\n' % (wzs_id, t))
        return False

def check_url(url):
    req = None
    try:
        req = urllib.urlopen(url)
        return req.getcode() == 200
    except:
        return False

def download_job( item, limit_speed = 0): 
    path = item['path']
    filename = item['filename']
    return_code1 = 0
    return_code2 = 0
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.path.isdir(path):
        os.remove(path)
        os.makedirs(path)

    if item.has_key('thumb') and item['thumb'] and check_url(item['thumb']):
        extension = os.path.splitext(item['thumb'])[-1]
        full_path = '%s/%s%s' % (path, filename, extension)
        if os.path.exists(full_path):
            os.remove(full_path)
        urllib.urlretrieve(item['thumb'], full_path)

    if item.has_key('video_url_n') and item['video_url_n'] and check_url(item['video_url_n']):
        filename_n = '%s_n.flv' % filename
        
        if item['firm'] == 'whole':
            print u'開始嘗試下載%s的%s委員會窄頻完整影片' % (item['date'], committee[item['comit_code']]['name'])
        elif item['firm'] == 'clip':
            print u'開始嘗試下載%s的%s委員會，第%s段%s窄頻發言片段' % (item['date'], committee[item['comit_code']]['name'], item['num'], item['speaker'])
        print u'影片網址為：%s' % item['video_url_n']
       
        return_code1 = download_adobe_hds(item['video_url_n'], filename_n, outdir=path, maxspeed=str(limit_speed))

        if not os.path.exists(os.path.join(path, filename_n)):
            sys.stderr.write('download_resource error, path: %s, video_url_n: %s\n' % (item['video_url_n'], item['filename']))
            sys.stderr.write(u'下載%s的%s委員會，第%s段%s窄頻發言片段失敗\n' % (item['date'], committee[item['comit_code']]['name'], item['num'], item['speaker']))
            return_code1 = 1


    if item.has_key('video_url_w') and item['video_url_w'] and check_url(item['video_url_w']):
        filename_w = '%s_w.flv' % filename
        
        if item['firm'] == 'whole':
            print u'開始嘗試下載%s的%s委員會寬頻完整影片' % (item['date'], committee[item['comit_code']]['name'])
        elif item['firm'] == 'clip':
            print u'開始嘗試下載%s的%s委員會，第%s段%s寬頻發言片段' % (item['date'], committee[item['comit_code']]['name'], item['num'], item['speaker'])
        print u'影片網址為：%s' % item['video_url_n']
        return_code2 = download_adobe_hds(item['video_url_w'], filename_w, outdir=path, maxspeed=str(limit_speed))
        if not os.path.exists(os.path.join(path, filename_w)):
            sys.stderr.write('download_resource error, path: %s, video_url_w: %s\n' % (item['video_url_w'], item['filename']))
            sys.stderr.write(u'下載%s的%s委員會，第%s段%s寬頻發言片段失敗\n' % (item['date'], committee[item['comit_code']]['name'], item['num'], item['speaker']))
            return_code2 = 1

    if return_code1 == 0 and return_code2 == 0:
        return 1
    else:
        return 0
