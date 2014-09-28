import subprocess


def download_adobe_hds(manifest_url, filename, **kwargs):

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

