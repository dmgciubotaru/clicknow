from http.server import BaseHTTPRequestHandler, HTTPServer, HTTPStatus
import requests
import logging
PORT_NUMBER = 8080

# This class will handle any incoming request from
# a browser

logging.basicConfig(level=logging.INFO, format='[%(name)s] > [%(levelname)s]\t%(message)s')
logger = logging.getLogger("hprox")

class myHandler(BaseHTTPRequestHandler):

    src_host = ("127.0.0.1",8080,"http")
    dst_host = ("docs.python.org",443,"https")


    def send_error(self, code, message=None, explain=None):
        logger.error(f"Request error {code}: {message} {explain}")
        super().send_error(code, message, explain)

    def log_message(self, format, *args):
        logger.info("%s - - [%s] %s" % (self.address_string(), self.log_date_time_string(), format % args))

    def handle_one_request(self):
        logger.info("="*20)
        logger.info("Request Started")

        super().handle_one_request()

        logger.info("Request Ended")
        logger.info("=" * 20)
        [logger.info("") for _ in range(3)]



    def __do_request(self):

        # Translate request URL
        url = f"{self.dst_host[2]}://{self.dst_host[0]}{self.path}"

        # Translate request headers
        self.headers["Host"] = f"{self.dst_host[0]}:{self.dst_host[1]}"

        print("Do req")
        # Do request
        res = requests.get(url, headers=self.headers, stream=True)
        print("Got req")
        # Translate response headers
        #if "Content-Encoding" in res.headers:
        #    del res.headers["Content-Encoding"]
        #res.headers["Content-Length"] = len(res.content)

        # Send response
        res.headers["Connection"] = "close"
        self.send_response(res.status_code)
        for header in res.headers:
            logger.debug(f"{header}: {res.headers[header]}")
            self.send_header(header, res.headers[header])
        self.end_headers()
        if "Content-Length" in res.headers:
            data = res.raw.read(int(res.headers["Content-Length"]))
            self.wfile.write(data)
        self.wfile.close()
        #print(f"Len = {len(data)}")


    def do_GET(self):
        self.__log_request()
        self.__do_request()
        return

    def __log_request(self):
        logger.debug(f"Client Address {self.client_address[0]}:{self.client_address[1]}")
        logger.debug(f"{self.command} {self.path} {self.request_version}")
        for header in self.headers:
            logger.debug(f"{header:20s}: {self.headers[header]}")


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print ('Started httpserver on port ' , PORT_NUMBER)

    # Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()