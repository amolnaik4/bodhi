#!/usr/bin/env python
import os
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

ROUTES = [
    ('/', '/bodhi_app/uploads')
]

class MyHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        root = os.getcwd()

        for patt, rootDir in ROUTES:
            if path.startswith(patt):                
                path = path[len(patt):]
                root = rootDir
                break

        return os.path.join(root, path)    

if __name__ == '__main__':
    httpd = HTTPServer(('0.0.0.0', 8000), MyHandler)
    httpd.serve_forever()
