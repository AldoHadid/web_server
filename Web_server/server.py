import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("Server now running... ", PORT)

httpd.serve_forever()
httpd.server_close()
print("Server stopped!")
