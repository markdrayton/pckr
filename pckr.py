#!/usr/bin/env python3

import argparse
import contextlib
import io
import json
import os.path
import urllib.parse
import re
import sys
from http.server import HTTPStatus, SimpleHTTPRequestHandler, ThreadingHTTPServer, test
from functools import partial

# Most of this is stolen/bodged from Lib/http/server.py.

class PicHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, regex, **kwargs):
        self.regex = re.compile(regex)
        super().__init__(*args, **kwargs)

    def send_head(self):
        path = self.translate_path(self.path)
        parts = urllib.parse.urlparse(path)
        dirname, pathname = os.path.split(parts.path)
        if pathname == "pckr.json":
            return self.list_directory_json(dirname)
        elif pathname == "":  # a directory
            path = "index.html"
            try:
                f = open(path, "rb")
            except OSError:
                self.send_error(HTTPStatus.NOT_FOUND, "File not found")
                return None
            fs = os.fstat(f.fileno())
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", self.guess_type(path))
            self.send_header("Content-Length", str(fs[6]))
            self.end_headers()
            return f
        return super().send_head()

    def list_directory_json(self, path):
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        list = [n for n in list if self.regex.search(n)]
        list.sort(key=lambda a: a.lower())

        enc = sys.getfilesystemencoding()
        out = json.dumps(list).encode(enc, 'surrogateescape')
        f = io.BytesIO()
        f.write(out)
        f.seek(0)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json; charset=%s" % enc)
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        return f

class DualStackServer(ThreadingHTTPServer):
    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(
                socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--port', type=int, default=8000, help="listen port")
    ap.add_argument('-r', '--regex', default="\.jpg", help="image match regex")
    ap.add_argument('directory', help="path to images")
    return ap.parse_args()

args = parse_args()

test(
    HandlerClass=partial(
        PicHTTPRequestHandler, directory=args.directory, regex=args.regex,
    ),
    ServerClass=ThreadingHTTPServer,
    port=args.port,
)
