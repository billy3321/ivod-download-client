import subprocess
import os.path


def download_adobe_hds(manifest_url, filename, **kwargs):

    outfile = filename
    if "outdir" in kwargs:
        outdir = kwargs["outdir"]

        if os.path.exists(outdir) and os.path.isdir(outdir):
            outfile = os.path.join(outdir, outfile)

    try:
        adobeHDS = AdobeHDS()
        adobeHDS.download(manifest_url, outfile)
        return 0
    except Exception as e:
        pass

    return 1


def _deprecated_download_adobe_hds(manifest_url, filename, **kwargs):

    cmd = ['php',
           'AdobeHDS.php',
           '--quality',
           'high',
           '--delete',
           '--manifest',
           manifest_url,
           '--outfile',
           filename]

    if "outdir" in kwargs:
        cmd.append("--outdir")
        cmd.append(kwargs["outdir"])

    if "maxspeed" in kwargs:
        cmd.append("--maxspeed")
        cmd.append(kwargs["maxspeed"])

    ret = subprocess.call(cmd)
    return ret


class AdobeHDS():

    def download(self, url, filename):
        from youtube_dl.downloader.f4m import *
        from youtube_dl import YoutubeDL

        ydl = YoutubeDL()
        info = {}
        info['url'] = u"%s" % url
        f4m = F4mFD(ydl, info)
        f4m.real_download(u"%s" % filename, info)
