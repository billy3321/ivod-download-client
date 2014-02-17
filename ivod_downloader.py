#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2
import json
import cookielib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import os
import sys
import subprocess
from optparse import OptionParser


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
    http_header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 'Host': 'ivod.ly.gov.tw'}
    req = urllib2.Request('http://ivod.ly.gov.tw/', None, http_header)
    web = urllib2.urlopen(req)
    result = web.read()
    #print result

def get_date_list(comt, limit=None):
    http_header = {'Referer': 'http://ivod.ly.gov.tw/Committee', 
        'Accept': '*/*',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 
        'Host': 'ivod.ly.gov.tw',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Pragma': 'no-cache'}
    req = urllib2.Request('http://ivod.ly.gov.tw/Committee/CommsDate', urllib.urlencode({'comtid': comt}), http_header)
    #try:
    web = urllib2.urlopen(req)
    if web.getcode() == 200:
        html = web.read()
        result = json.loads(html)
        date_list = []
        for i in result['mdate']:
            if not limit:
                date_list.append(i['METDAT'])
            elif limit:
                if i['METDAT'] > limit:
                    date_list.append(i['METDAT'])
        return date_list
    else:
        return False
    #except:
    #    return False

def get_movie_by_date(comit, date, page=1):
    http_header = {'Referer': 'http://ivod.ly.gov.tw/Committee', 
        'Accept': '*/*',
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)', 
        'Host': 'ivod.ly.gov.tw',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Pragma': 'no-cache'}
    req = urllib2.Request('http://ivod.ly.gov.tw/Committee/MovieByDate', urllib.urlencode({'comtid': comit, 'date': date, 'page': page}), http_header)
    #try:
    web = urllib2.urlopen(req)
    if web.getcode() == 200:
        html_result = web.read()
        #print html_result
        result = json.loads(html_result)
        return result
        #Find WZS_ID
    else:
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
    web = urllib2.urlopen(req)
    #print web.getcode()
    if web.getcode() == 200:
        html_result = web.read()
        #print html_result
        xml = BeautifulSoup(html_result)
        div_movie = xml.find('div', {'class': 'movie'})
        if div_movie:
            #print div_movie
            script_text = div_movie.find('script').text
            script_text = script_text.replace("readyPlayer('http://ivod.ly.gov.tw/public/scripts/','", '')
            script_text = script_text.replace("');", '')
            print script_text
            return script_text
        #return xml

def get_picture_url(pic_name):
    return 'http://ivod.ly.gov.tw/Image/Pic/' + pic_name

def download_resource(item): 
    path = os.path.join('data', item['ad'], item['session'], committee[item['comit_code']]['code'], item['date'])
    filename = '%s-%s' % (item['date'], committee[item['comit_code']]['code'])
    if item.has_key('speaker'):
        filename += '-%s-%s' % (item['order'], item['speaker'])
    if not os.path.exists(path):
        os.makedirs(path)
    elif not os.path.isdir(path):
        os.remove(path)
        os.makedirs(path)

    if item.has_key('thumb') and item['thumb'] and check_url(item['thumb']):
        extension = os.path.splitext(item['thumb'])[1]
        full_path = '%s/%s%s' % (path, filename, extension)
        cmd = "wget -O '%s' '%s'" % (full_path, item['thumb'])
        #print cmd
        #os.system(cmd)
        urllib.urlretrieve(item['thumb'], full_path)

    if item.has_key('video_url_n') and item['video_url_n'] and check_url(item['video_url_n']):
        #extension = 'mp4'
        filename_n = '%s_n' % filename
        cmd = "php AdobeHDS.php  --quality high --delete --manifest '%s' --outdir %s --outfile %s" % (item['video_url_n'], path, filename_n)
        #print cmd
        os.system(cmd)

    if item.has_key('video_url_w') and item['video_url_w'] and check_url(item['video_url_w']):
        #extension = 'mp4'
        filename_w = '%s_w' % filename
        cmd = "php AdobeHDS.php  --quality high --delete --manifest '%s' --outdir %s --outfile %s" % (item['video_url_w'], path, filename_w)
        #print cmd
        os.system(cmd)

def write_config(info):
    path = os.path.join('data', info['whole'][0]['ad'], info['whole'][0]['session'], committee[info['whole'][0]['comit_code']]['code'], info['whole'][0]['date'])
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = os.path.join(path, 'info.json')
    if os.path.exists(full_path):
        os.remove(full_path)
    with open(full_path, 'w') as f:
        f.write(json_dumps(info) + '\n')

def test_php():
    cmd = 'php test_ext.php'
    result = os.system(cmd)
    return result == 0

def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-l", "--limit-date", dest="limit_date",
                      help='get video after date, format is %Y-%m-%d')
    parser.add_option("-n", "--no-download",
                      action="store_true", dest="nd", help="don't download resource")
    (options, args) = parser.parse_args()
    print options
    if not test_php():
        print "Please check PHP extensions."
        sys.exit(1)
    for comit_id in committee.keys():
        date_list = get_date_list(comit_id, options.limit_date)
        print date_list
        for date in date_list:
            movie_list = get_movie_by_date(comit_id, date, 1)
            page_num = (int(movie_list['total']) / 5) + 1
            full_list = []
            single_list = []
            for i in movie_list['full']:
                #print i
                item = {}
                item['ad'] = i['STAGE_']
                item['session'] = i['DUTION']
                item['sitting'] = None
                item['wmvid'] = i['MEREID']
                item['time'] = i['ST_TIM']
                item['video_url_n'] = get_movie_url(i['MEREID'], 'whole', 'n')
                item['video_url_w'] = get_movie_url(i['MEREID'], 'whole', 'w')
                item['date'] = i['ST_TIM'].split(' ')[0]
                item['summary'] = i['METDEC']
                item['comit_code'] = comit_id
                full_list.append(item)
                #print item
                if not options.nd:
                    download_resource(item)
            for num in xrange(1, (page_num + 1)):
                if num != 1:
                    movie_list = get_movie_by_date(comit_id, date, num)
                for i in movie_list['result']:
                    item = {}
                    #print i
                    item['ad'] = i['STAGE_']
                    item['session'] = i['DUTION']
                    item['sitting'] = None
                    item['length'] = i['MOVTIM']
                    item['wmvid'] = i['WZS_ID']
                    item['video_url_n'] = get_movie_url(i['WZS_ID'], 'clip', 'n')
                    item['video_url_w'] = get_movie_url(i['WZS_ID'], 'clip', 'w')
                    item['speaker'] = i['CH_NAM']
                    item['thumb'] = get_picture_url(i['PHOTO_'])
                    item['time'] = i['ST_TIM']
                    item['date'] = i['ST_TIM'].split(' ')[0]
                    item['summary'] = i['METDEC']
                    item['order'] = i['R']
                    item['comit_code'] = comit_id
                    single_list.append(item)
                    #print item
                    if not options.nd:
                        download_resource(item)
            #print full_list
            print single_list
            full_info = {'whole': full_list, 'clips': single_list}
            write_config(full_info)


if __name__ == '__main__':
    main()
