from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl
import sys
import base64

key = ''

class MyHandler(SimpleHTTPRequestHandler):
    def do_HEAD(self, authenticated):
        if authenticated:
            self.send_response(200)
        else:
            self.send_response(401)
            self.send_header('WWW-Authenticate','Basic realm=\"Secure Share\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.headers.get('Authorization') == 'Basic '+key.decode('utf-8'):
            SimpleHTTPRequestHandler.do_GET(self)
            pass
        elif self.headers.get('Authorization') == None:
            self.do_HEAD(False)
            self.wfile.write(bytes('Anmeldung fehlgeschlagen', 'utf-8'))
            pass
        else:
            self.do_HEAD(False)
            self.wfile.write(bytes('Anmeldung fehlgeschlagen', 'utf-8'))
            pass

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 adhocserver.py [username] [password] " +\
              "[certdir] [port (opt.)]")
        return
    
    global key
    username = sys.argv[1]
    password = sys.argv[2]
    certdir = sys.argv[3]
    port = int(sys.argv[4]) if len(sys.argv) == 5 else 4443
    credentials = '{0}:{1}'.format(username, password)
    key = base64.b64encode(bytes(credentials, 'utf-8'))
    CERTFILE = certdir + 'cert.pem'
    KEYFILE = certdir + 'key.pem'
    
    httpd = HTTPServer(('localhost', port), MyHandler)

    httpd.socket = ssl.wrap_socket (httpd.socket, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)

    httpd.serve_forever()
    
if __name__ == '__main__':
    main()
