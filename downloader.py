import subprocess


def download_adobe_hds(manifest_url, filename, **kwargs):
    ret = subprocess.call(['php',
                           'AdobeHDS.php',
                           '--quality',
                           'high',
                           '--delete',
                           '--manifest',
                           manifest_url,
                           '--outfile',
                           filename])
    return ret
