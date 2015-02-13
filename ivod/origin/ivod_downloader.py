#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, urllib, urllib2, json, cookielib, sys, random, time, datetime, subprocess
from BeautifulSoup import BeautifulSoup, SoupStrainer
from optparse import OptionParser
from downloader import download_adobe_hds

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))

import db

reload(sys)
sys.setdefaultencoding('utf-8')

currect_time = 0
base_url = 'http://ivod.ly.gov.tw/'
committee_url = 'http://ivod.ly.gov.tw/Committee/CommsDate'

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

def config_parser(path):
    """parser the config"""
    try:
        with open(path) as json_data:
            data = json.load(json_data)
        return data
    except:
        return False

def json_dumps(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False).encode('utf8')

def check_url(url):
    req = None
    try:
        req = urllib.urlopen(url)
        return req.getcode() == 200
    except:
        return False

def init_cookie():
    cookie=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    reset_cookie()

def reset_cookie():
    global currect_time
    #if time lagger then 15 min, will reset.
    if time.time() - currect_time > 900:
        http_header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Host': 'ivod.ly.gov.tw'}
        req = urllib2.Request('http://ivod.ly.gov.tw/', None, http_header)
        try:
            web = urllib2.urlopen(req)
            result = web.read()
            currect_time = time.time()
        except:
            sys.stderr.write('reset cookie error\n')
            return False
        #print result

def get_date_list(comt, start_date=None, end_date=None):
    http_header = {'Referer': 'http://ivod.ly.gov.tw/Committee', 
        'Accept': '*/*',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 
        'Host': 'ivod.ly.gov.tw',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Pragma': 'no-cache'}
    req = urllib2.Request('http://ivod.ly.gov.tw/Committee/CommsDate', urllib.urlencode({'comtid': comt}), http_header)
    try:
        if not start_date:
            start_date = '2011-01-01'
        if not end_date:
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        web = urllib2.urlopen(req)
        if web.getcode() == 200:
            html = web.read()
            #print type(html)
            #print html
            html = html.decode('utf-8-sig')
            result = json.loads(html)
            date_list = []
            for i in result['mdate']:
                if end_date >= i['METDAT'] >= start_date:
                    date_list.append(i['METDAT'])
            return date_list
        else:
            sys.stderr.write('get_date_list content error, comtid: %s\n' % comt)
            return False
    except:
        sys.stderr.write('get_date_list web error, comtid: %s\n' % comt)
        reset_cookie()
        return False

def get_movie_by_date(comit, date, page=1):
    http_header = {'Referer': 'http://ivod.ly.gov.tw/Committee', 
        'Accept': '*/*',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 
        'Host': 'ivod.ly.gov.tw',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Pragma': 'no-cache'}
    req = urllib2.Request('http://ivod.ly.gov.tw/Committee/MovieByDate', urllib.urlencode({'comtid': comit, 'date': date, 'page': page}), http_header)
    try:
        web = urllib2.urlopen(req)
    except:
        sys.stderr.write('get_movie_by_date web error, comit: %s, date: %s\n' % (comit, date))
        reset_cookie()
        return False
    if web.getcode() == 200:
        html_result = web.read()
        html_result = html_result.decode('utf-8-sig')
        #print html_result
        result = json.loads(html_result)
        return result
        #Find WZS_ID
    else:
        sys.stderr.write('get_movie_by_date content error, comit: %s, date: %s\n' % (comit, date))
        return False

def get_movie_url(wzs_id, t, quality='w'):
    http_header = {'Referer': 'http://ivod.ly.gov.tw/Committee', 
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 
        'Host': 'ivod.ly.gov.tw',
        'Connection': 'keep-alive'}
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
    #print url
    req = urllib2.Request(url, None, http_header)
    try:
        web = urllib2.urlopen(req)
    except:
        random_sleep()
        sys.stderr.write('get_movie_url web error, wzs_id: %s, t: %s\n' % (wzs_id, t))
        reset_cookie()
        return False
    #print web.getcode()
    if web.getcode() == 200:
        html_result = web.read()
        #print html_result
        xml = BeautifulSoup(html_result)
        div_movie = xml.find('div', {'class': 'video'})
        if not div_movie:
            div_movie = xml.find('div', {'class': 'video-box'})
        #print div_movie
        if div_movie:
            #print div_movie
            script_text = div_movie.find('script').text.strip()
            script_text = script_text.replace("readyPlayer('http://ivod.ly.gov.tw/public/scripts/','", '')
            script_text = script_text.split("');")[0]
            #print script_text
            return script_text
        #return xml
    else:
        sys.stderr.write('get_movie_url content error, wzs_id: %s, t: %s\n' % (wzs_id, t))
        return False

def get_picture_url(pic_name):
    return 'http://ivod.ly.gov.tw/Image/Pic/' + pic_name

def random_sleep():
    time.sleep(random.randint(1,5))

def download_resource(item, limit_speed = 0): 
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
    

def write_config(info, path):
    #print info
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = os.path.join(path, 'info.json')
    if os.path.exists(full_path):
        os.remove(full_path)
    with open(full_path, 'w') as f:
        f.write(json_dumps(info) + '\n')


def check_file_downloaded(path, filename):
    if os.path.exists(os.path.join(path, filename)):
        return 1
    else:
        return 0

def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-s", "--start-date", dest="start_date",
                      help='get video after date, format is %Y-%m-%d')
    parser.add_option("-e", "--end-date", dest="end_date",
                      help='get video before date, format is %Y-%m-%d')
    parser.add_option("-c", "--committee", dest="comit_code",
                      help='parse committee, please input code.')
    parser.add_option("-n", "--no-download",
                      action="store_true", dest="nd", help="don't download resource")
    parser.add_option("-l", "--limit-speed", dest="limit_speed",
                      help='download speed, unit is kb/s')
    (options, args) = parser.parse_args()
    #print options
    if options.start_date:
        try:
            start_date = datetime.datetime.strptime(options.start_date, '%Y-%m-%d')
            start_date = start_date.strftime('%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    else:
        start_date = None
    if options.end_date:
        try:
            end_date = datetime.datetime.strptime(options.end_date, '%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    else:
        end_date = None

    if options.comit_code:
        comit_code = options.comit_code
    else:
        comit_code = None

    if not options.limit_speed:
        limit_speed = 0
    else:
        limit_speed = options.limit_speed

    config = config_parser('config.json')

    if not config:
        print 'config error.'
        sys.exit(1)
    database = db.Database(config['db'])

    for comit_id in committee.keys():
        reset_cookie()
        if not comit_code or comit_code == committee[comit_id]['code']:
            print u'開始掃描%s委員會可以抓取的影片...' % committee[comit_id]['name']
            date_list = get_date_list(comit_id, start_date, end_date)
            if not date_list:
                date_list = []
            date_list.sort(reverse=True)
            print date_list
            for date in date_list:
                reset_cookie()
                random_sleep()
                movie_list = get_movie_by_date(comit_id, date, 1)
                page_num = (int(movie_list['total']) / 5) + 1
                full_list = []
                single_list = []
                for i in movie_list['full']:
                    #print i
                    item = {}
                    item['firm'] = 'whole'
                    item['wmvid'] = i['MEREID']
                    item['ad'] = i['STAGE_']
                    item['session'] = i['DUTION']
                    item['sitting'] = None
                    item['time'] = i['ST_TIM'].split(' ')[1]
                    item['video_url_n'] = get_movie_url(i['MEREID'], 'whole', 'n')
                    item['video_url_w'] = get_movie_url(i['MEREID'], 'whole', 'w')
                    item['date'] = i['ST_TIM'].split(' ')[0]
                    item['summary'] = i['METDEC'].replace('\n', '')
                    item['comit_code'] = comit_id
                    item['filename'] = '%s-%s' % (item['date'], committee[item['comit_code']]['code'])
                    item['path'] = os.path.join(config['download']['path'], item['ad'], item['session'], committee[item['comit_code']]['code'], item['date'])
                    item['num'] = None
                    item['ext'] = 'flv'
                    item['length'] = None
                    item['speaker'] = None
                    item['thumb'] = None
                    if check_file_downloaded(item['path'], (item['filename'] + '_n.flv')) and check_file_downloaded(item['path'], (item['filename'] + '_w.flv')):
                        item['finished'] = 1
                    else:
                        item['finished'] = 0
                    #item['finished'] = database.query_if_finished(item)
                    full_list.append(item)
                    random_sleep()
                    #print item
                    if not options.nd and not item['finished']:
                        item['finished'] = download_resource(item, limit_speed)
                        random_sleep()
                        #retry once
                        if not item['finished']:
                            item['finished'] = download_resource(item, limit_speed)
                            random_sleep()
                    database.insert_data(item)
                for num in xrange(1, (page_num + 1)):
                    if num != 1:
                        movie_list = get_movie_by_date(comit_id, date, num)
                    for i in movie_list['result']:
                        item = {}
                        #print i
                        item['wmvid'] = i['WZS_ID']
                        item['firm'] = 'clip'
                        item['ad'] = i['STAGE_']
                        item['session'] = i['DUTION']
                        item['sitting'] = None
                        item['length'] = i['MOVTIM']
                        item['video_url_n'] = get_movie_url(i['WZS_ID'], 'clip', 'n')
                        item['video_url_w'] = get_movie_url(i['WZS_ID'], 'clip', 'w')
                        item['speaker'] = i['CH_NAM']
                        item['thumb'] = get_picture_url(i['PHOTO_'])
                        item['time'] = i['ST_TIM'].split(' ')[1]
                        item['date'] = i['ST_TIM'].split(' ')[0]
                        item['summary'] = i['METDEC'].replace('\n', '')
                        item['num'] = i['R']
                        item['comit_code'] = comit_id
                        item['ext'] = 'flv'
                        item['filename'] = '%s-%s-%s-%s' % (item['date'], committee[item['comit_code']]['code'], item['num'], item['speaker'])
                        item['path'] = os.path.join(config['download']['path'], item['ad'], item['session'], committee[item['comit_code']]['code'], item['date'])
                        #item['finished'] = database.query_if_finished(item)
                        if check_file_downloaded(item['path'], (item['filename'] + '_n.flv')) and check_file_downloaded(item['path'], (item['filename'] + '_w.flv')):
                            item['finished'] = 1
                        else:
                            item['finished'] = 0
                        single_list.append(item)
                        random_sleep()
                        #print item
                        if not options.nd and not item['finished']:
                            item['finished'] = download_resource(item, limit_speed)
                            random_sleep()
                            #retry once
                            if not item['finished']:
                                item['finished'] = download_resource(item, limit_speed)
                                random_sleep()
                        database.insert_data(item)
                #print full_list
                #print single_list
                full_info = {'whole': full_list, 'clips': single_list}
                write_config(full_info, config['download']['path'])


if __name__ == '__main__':
    main()
