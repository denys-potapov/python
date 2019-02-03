#!/usr/bin/env python
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from game.game import Game


class Handler(BaseHTTPRequestHandler):
    game = Game()

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        payload = self.rfile.read(int(self.headers['Content-Length']))

        # Hive object from request payload
        hive = json.loads(payload.decode('utf-8').lower())

        orders = self.game.do_turn(hive)

        response = json.dumps(orders)

        try:  # For python 3
            out = bytes(response, "utf8")
        except TypeError:  # For python 2
            out = bytes(response)

        self.wfile.write(out)

        print("Trick:",  hive['tick'], response)


def run():
    server_address = ('0.0.0.0', 7070)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()

run()
