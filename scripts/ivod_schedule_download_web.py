import SimpleHTTPServer
import SocketServer
import StringIO

import json
from ivod.downloader import download_adobe_hds
from ivod.ivod_parser import extract_manifest_from_player_page
from multiprocessing import Process

def fork_to_download(data):
    info = data[1]
    download_adobe_hds(info['manifest'], info['filename'])

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def get_ivod_playurl(self, uri):
        if "/Play/VOD" not in uri:
            return None

        if "http://" not in uri:
            uri = "http://ivod.ly.gov.tw" + uri

        idx = uri.index("http://") 
        if idx != 0:
            uri = uri[idx:]

        print "sss", uri
        return uri, extract_manifest_from_player_page(uri)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        info = self.get_ivod_playurl(self.path)
        p = Process(target=fork_to_download, args=(info,))
        p.start()
        self.wfile.write(json.dumps(info))


print('Server listening on port 8000...')
httpd = SocketServer.TCPServer(('', 8000), Handler)
httpd.serve_forever()
