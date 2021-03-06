from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime

logfile = open('/log/access.log',"a")

def log(msg):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    logfile.write(f"[{date_time}] {msg}\n")
    logfile.flush()
    print(f"[{date_time}] {msg}")


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        log(f"Connection from {self.client_address}")
        log(f"Requested path {self.path}")
        for header in self.headers:
            log(f"{header}:{self.headers['header']}")
        try:
            uri = self.path
            parsed = urlparse.urlparse(uri)
            args = parse_qs(parsed.query)
            token = args["tkn"][0]
            new_location = args["loc"][0]
            log(f"RequestData: {{\"{token}\", \"{new_location}\"}}")
        except:
            log(f"Error in parsing the request")
            new_location = "http://www.google.com"

        self.send_response(301)
        self.send_header("Location", new_location)
        self.end_headers()
        log("Done\n\n\n")

    def log_message(self, format, *args):
        return

def run():
    server_address = ('', 80)
    httpd = HTTPServer(server_address, HttpHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    run()