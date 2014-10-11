from downloader import download_adobe_hds
from ivod_parser import extract_manifest_from_player_page

def download_single_high_quality_video(url):
    play_info = extract_manifest_from_player_page(
        url,
        ensure_high_quality_video=True)

    if play_info:
        return download_adobe_hds(play_info['manifest'], play_info['filename'])
    else:
        sys.stderr.write('get_movie_url content error')
        return False
