import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import sys

# -----------
# important : for testing SameGame project,
# move this file one folder above -> ../
# this is due to the fact that katagames-sdk is not located in the current dir!
# -----------

PORT = 8000 if len(sys.argv) < 2 else int(sys.argv[1])

Handler = http.server.SimpleHTTPRequestHandler

Handler.extensions_map={
    '.manifest': 'text/cache-manifest',
    '.html': 'text/html',
    '.txt': 'text/plain',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.svg': 'image/svg+xml',
    '.css': 'text/css',
    '.js': 'application/x-javascript',
    '.json': 'application/json',
    '.xml': 'application/xml',
    '.wasm': 'application/wasm',
    '': 'application/octet-stream', # Default
}

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)
print("serving at http://0.0.0.0:{}/".format(PORT))
httpd.serve_forever()
