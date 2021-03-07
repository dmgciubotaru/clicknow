from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime
from dbaccess import DBConn
import time
import os
import sys
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(module)s:%(levelname)s]: %(message)s")

log = logging.getLogger("main")

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        log.info(f"Request: ({self.client_address})>{self.path}")
        for header in self.headers:
            log.info(f"\t{header}:{self.headers['header']}")
        #try:
        uri = self.path
        parsed = urlparse.urlparse(uri)
        args = parse_qs(parsed.query)
        token = args.get("tkn",[None])[0]
        new_location = args.get("loc",[None])[0]
        log.info(f"RequestData: {{\"{token}\", \"{new_location}\"}}")
        if all([x is not None for x in [token, new_location]]):
            conn.add_clicklog_entry(token, str(self.client_address), {k: v for k, v in self.headers.items()})
            logging.info("Access registered in clicklog")
        else:
            new_location = "https://www.google.com/"
            logging.warning("Invalid request")

        self.send_response(302)
        self.send_header("Location", new_location)
        self.end_headers()
        log.info(f"Redirected to {new_location}\n\n\n")

    def log_message(self, format, *args):
        return

def run():
    port = 80
    log.info(f"Starting HTTP server on port {port}")
    server_address = ('', port)
    httpd = HTTPServer(server_address, HttpHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    db_host,db_port = os.getenv("PG_HOST","localhost"),int(os.getenv("PG_PORT","5432"))
    conn = DBConn(db_host, db_port)
    run()