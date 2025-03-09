import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler


class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.client_address[0] != '127.0.0.1':
            self.send_response(403)
            self.end_headers()
            return

        if self.path == '/':
            self.path = '/index.html'
        if self.path == '/overlayPicture.png':
            self.path = '/input/overlayPicture.png'
        else:
            self.path = '/serv' + self.path
        try:
            with open(self.path[1:], 'rb') as content:
                self.send_response(200)
                self.end_headers()
                shutil.copyfileobj(content, self.wfile)

        except:
            file_to_open = "File not found"
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(file_to_open, 'utf-8'))


httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()
