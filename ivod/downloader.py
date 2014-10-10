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


class AdobeHDS():

    def download(self, url, filename):
        from youtube_dl.downloader.f4m import F4mFD
        from youtube_dl import YoutubeDL

        ydl = YoutubeDL()
        info = {}
        info['url'] = u"%s" % url
        f4m = F4mFD(ydl, info)
        f4m.real_download(u"%s" % filename, info)
