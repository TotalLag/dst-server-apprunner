import http.server
import socketserver
import subprocess

PORT = 8080

class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/health':
            # Check if the DST server process is running
            try:
                subprocess.check_output(["pgrep", "-f", "dontstarve_dedicated_server_nullrenderer"])
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'OK')
            except subprocess.CalledProcessError:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'DST server not running')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not Found')

with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
    print(f"Serving health check at port {PORT}")
    httpd.serve_forever()