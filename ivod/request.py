import json
import urllib
import urllib2


class PresetURL(object):

    COMMS_DATE = 'http://ivod.ly.gov.tw/Committee/CommsDate'
    MOVIE_BY_DATE = 'http://ivod.ly.gov.tw/Committee/MovieByDate'


def _default_header():
    header = {'Referer': 'http://ivod.ly.gov.tw/Committee',
              'Accept': '*/*',
              'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
              'Host': 'ivod.ly.gov.tw',
              'Connection': 'keep-alive',
              'X-Requested-With': 'XMLHttpRequest',
              'Pragma': 'no-cache'}

    return header


def enocded_request_body(data=None):
    if data:
        return urllib.urlencode(data)
    return None


def build_header(header):
    if header:
        return header
    return _default_header()


def build_request(url, data=None, header=None):
    req = urllib2.Request(
        url,
        enocded_request_body(data),
        build_header(header))
    return req


def get_content(url_or_alias, data=None):
    url = url_or_alias
    if url_or_alias in PresetURL.__dict__:
        url = PresetURL.__dict__[url_or_alias]
    req = build_request(url, data)

    try:
        resp = urllib2.urlopen(req)
        if resp.code == 200:
            return resp.read().decode('utf-8-sig')
    except Exception as e:
        pass

    return None


def get_json_content(url_or_alias, data=None):
    content = get_content(url_or_alias, data)
    if content:
        return json.loads(content)
    return None
