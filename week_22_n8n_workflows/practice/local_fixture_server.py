"""Read-only local HTTP fixture. No external API, no credentials, no writes."""
import argparse
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer

PAYLOAD = (Path(__file__).resolve().parents[1] / 'datasets' / 'http_response_fixture.json').read_bytes()
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/tickets':
            status, body = 200, PAYLOAD
        elif self.path == '/simulate-503':
            status, body = 503, b'{"error":"simulated_service_failure"}'
        else:
            status, body = 404, b'{"error":"not_found"}'
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, format, *args):
        pass  # Synthetic lab: suppress access logs.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    print(f'Fixture server on http://{args.host}:{args.port}; Ctrl+C stops.')
    HTTPServer((args.host, args.port), Handler).serve_forever()
