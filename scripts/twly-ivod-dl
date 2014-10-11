#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from optparse import OptionParser
from ivod.downloader import download_adobe_hds
from ivod.ivod_parser import extract_manifest_from_player_page

reload(sys)
sys.setdefaultencoding('utf-8')


def download_from_url(url):
    play_info = extract_manifest_from_player_page(
        url,
        ensure_high_quality_video=True)

    if play_info:
        return download_adobe_hds(play_info['manifest'], play_info['filename'])
    else:
        sys.stderr.write('get_movie_url content error')
        return False


def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-u", "--url", dest="url",
                      help='IVOD Url')
    (options, args) = parser.parse_args()

    if not options.url:
        print 'Please input url.'
        sys.exit(1)
    download_from_url(options.url)


if __name__ == '__main__':
    main()
