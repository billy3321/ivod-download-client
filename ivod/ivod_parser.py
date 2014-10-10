# -*- coding: utf-8 -*-
import urllib2
from request import build_request
from BeautifulSoup import BeautifulSoup


_SCRIPT_PLAYER_DELIMITER = "readyPlayer('http://ivod.ly.gov.tw/public/scripts/','"


def _extract_manifest_from_player_script(content):
    content = content.replace(_SCRIPT_PLAYER_DELIMITER, '')
    content = content.replace("');", '')

    return content


def _extract_text_info_from_player_page(url, content):
    meet = None
    name = None
    date = None
    filename = None

    if 'VOD' in url:
        meet = content.find('h4').text.replace(
            u'會議別 ：',
            u'').replace(
            u'委員會',
            u'')
        name = content.findAll('p')[1].text.replace(u'委  員  名  稱：', u'')
        date = content.findAll('p')[4].text.replace(
            u'會  議  時  間：',
            u'').split(' ')[0]
        filename = '%s_%s_%s.flv' % (date, meet, name)
    elif 'FULL' in url:
        meet = content.find('h4').text.replace(
            u'會議別 ：',
            u'').replace(
            u'委員會',
            u'')
        date = content.findAll('p')[1].text.replace(
            u'會  議  時  間：',
            u'').split(' ')[0]
        filename = '%s_%s.flv' % (date, meet)

    return {'filename': filename, 'date': date, 'name': name, 'meet': meet}

def _supported_url(url):
    return 'http://ivod.ly.gov.tw/Play/' in url


def extract_manifest_from_player_page(url, ensure_high_quality_video=False):

    if not _supported_url(url):
        return None

    if ensure_high_quality_video:
        url = url.replace('300K', '1M')

    req = build_request(url, None)
    try:
        resp = urllib2.urlopen(req)
        if resp.code != 200:
            return None

        content = resp.read()
        xml = BeautifulSoup(content)
        div_movie = xml.find('div', {'class': 'movie'})

        movie_info = xml.find(
            'div', {
                'class': 'movie_box clearfix'}).find(
            'div', {
                'class': 'text'})
        info = _extract_text_info_from_player_page(url, movie_info)

        if not div_movie:
            div_movie = xml.find('div', {'class': 'movie_large'})

        if div_movie:
            script_text = div_movie.find('script').text
            info['manifest'] = _extract_manifest_from_player_script(
                script_text)
            return info
    except Exception as e:
        raise e
        pass

    return None
